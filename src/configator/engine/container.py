#!/usr/bin/env python3

import logging
import threading
import time

from deepdiff import DeepDiff
from readerwriterlock import rwlock
from typing import Callable, Dict, List, Optional, Union

from configator.engine.observer import CapsuleObservable
from configator.utils.datatype_util import get_type_fullname
from configator.utils.function_util import json_loads

LOG = logging.getLogger(__name__)

class SettingCapsule(CapsuleObservable):
    __label = None
    __default = None
    __default_initial = False
    __setting = None
    __setting_state = None
    __context = None
    __context_state = None
    __loader = None
    __transformer = None
    __on_access = None
    __on_pre_load = None
    __on_post_load = None
    __on_load_error = None
    __on_refresh = None
    #
    #
    def __init__(self, label: str, loader: Callable, transformer:Callable=None, default=None, lazy_load:bool=True,
            on_access:Optional[Callable]=None,
            on_pre_load:Optional[Callable]=None,
            on_post_load:Optional[Callable]=None,
            on_load_error:Optional[Callable]=None,
            on_use_default:Optional[Callable]=None,
            on_refresh:Optional[Callable]=None):
        assert isinstance(label, str) and label, "[label] must be a string and not empty"
        self.__label = label
        #
        assert callable(loader), "[loader] must be a function"
        self.__loader = loader
        #
        assert transformer is None or callable(transformer), "[transformer] must be a function"
        self.__transformer = transformer
        #
        if default is not None:
            self.__default = default
            self.__default_initial = True
        #
        self.__setting = None
        self.__setting_state = 0
        self.__context = None
        self.__context_state = 0
        #
        if callable(on_access):
            self.__on_access = on_access
        #
        if callable(on_pre_load):
            self.__on_pre_load = on_pre_load
        else:
            self.__on_pre_load = default_on_pre_load
        #
        if callable(on_post_load):
            self.__on_post_load = on_post_load
        else:
            self.__on_post_load = default_on_post_load
        #
        if callable(on_load_error):
            self.__on_load_error = on_load_error
        else:
            self.__on_load_error = default_on_load_error
        #
        if callable(on_use_default):
            self.__on_use_default = on_use_default
        else:
            self.__on_use_default = default_on_use_default
        #
        if callable(on_refresh):
            self.__on_refresh = on_refresh
        else:
            self.__on_refresh = default_on_refresh
        #
        self.__load_lock = threading.RLock()
        self.__rwhandler = rwlock.RWLockFairD()
        #
        if not lazy_load:
            self.payload()
        #
        self._observe()
    #
    #
    def summarize(self, *args, deepdiff=True, show_default=False, show_setting=False, **kwargs):
        info = dict(
            context=dict(
                type=get_type_fullname(self.context),
                state=self.__context_state
            ),
            setting=dict(
                type=get_type_fullname(self.setting),
                state=self.__setting_state
            ),
            default=dict(
                initial=self.__default_initial
            )
        )
        #
        if show_setting:
            info['setting']['value'] = self.setting
        #
        if show_default:
            info['default']['value'] = self.__default
        #
        if deepdiff and isinstance(self.__default, dict) and isinstance(self.setting, dict):
            try:
                obj, err = json_loads(DeepDiff(dict(self.__default), dict(self.setting), ignore_order=True).to_json())
                if err:
                    info['setting']['diff'] = dict(error=str(err))
                else:
                    info['setting']['diff'] = obj
            except Exception as err:
                if LOG.isEnabledFor(logging.ERROR):
                    LOG.log(logging.ERROR, 'SettingCapsule[%s] is error on comparing the setting value and the default', self.label)
        #
        return info
    #
    #
    @property
    def label(self):
        return self.__label
    #
    @property
    def content(self):
        return self.get_setting()
    #
    def payload(self, *args, **kwargs):
        return self.get_setting(*args, **kwargs)
    #
    @property
    def setting(self):
        return self.get_setting()
    #
    def get_setting(self, *args, **kwargs):
        setting, _ = self.__read(*args, **kwargs)
        return setting
    #
    @property
    def setting_state(self):
        return self.__setting_state
    #
    #
    @property
    def context(self):
        return self.get_context()
    #
    def get_context(self, *args, **kwargs):
        _, context = self.__read(*args, **kwargs)
        return context
    #
    @property
    def context_state(self):
        return self.__context_state
    #
    #
    def __read(self, *args, **kwargs):
        with self.__rwhandler.gen_rlock():
            if callable(self.__on_access):
                self.__on_access(self.__label)
            if self.__setting is None:
                with self.__load_lock:
                    if self.__setting is None:
                        self.__setting_state = 0
                        self.__setting, self.__setting_state = self.__reload(*args, **kwargs)
                        self.__context = None
                    if self.__context is None:
                        self.__context_state = 0
                        self.__context, self.__context_state = self.__retransform(self.__setting)
            return self.__setting, self.__context
    #
    def refresh(self, parameters: Optional[Union[Dict,List]] = None, lazy_load:bool=False, **kwargs):
        with self.__rwhandler.gen_wlock():
            if callable(self.__on_refresh):
                self.__on_refresh(self.__label)
            #
            self.__context = None
            self.__context_state = 0
            self.__setting = None
            self.__setting_state = 0
            #
            if not lazy_load:
                args = []
                kwargs = {}
                if isinstance(parameters, dict):
                    kwargs = parameters
                elif isinstance(parameters, list):
                    args = parameters
                self.__setting, self.__setting_state = self.__reload(*args, **kwargs)
                self.__context, self.__context_state = self.__retransform(self.__setting)
        return self
    #
    #
    def reset(self, parameters: Optional[Union[Dict,List]] = None, lazy_load:bool=False, **kwargs):
        return self.refresh(parameters, lazy_load=lazy_load, **kwargs)
    #
    #
    def __reload(self, *args, **kwargs):
        try:
            if callable(self.__on_pre_load):
                self.__on_pre_load(self.__label)
            #
            result = self.__loader(*args, **kwargs, __content__=self.__setting)
            #
            if callable(self.__on_post_load):
                self.__on_post_load(self.__label)
            #
            if result is not None:
                return result, 2
        except Exception as exception:
            if callable(self.__on_load_error):
                self.__on_load_error(self.__label, error=exception)
            if self.__default is None:
                raise exception
        #
        if callable(self.__on_use_default):
            self.__on_use_default(self.__label, default=self.__default)
        return self.__default, 1
    #
    #
    def __retransform(self, setting):
        if self.__transformer is None:
            return setting, 1
        #
        try:
            context = self.__transformer(setting, __context__=self.__context)
            return context, 2
        except Exception as exception:
            raise exception


def default_on_refresh(label, *args, **kwargs):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] refresh the content', label)

def default_on_pre_load(label, *args, **kwargs):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] invoke the loader to load the content', label)

def default_on_post_load(label, *args, **kwargs):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] loading has finished', label)

def default_on_load_error(label, error, *args, **kwargs):
    if LOG.isEnabledFor(logging.ERROR):
        LOG.log(logging.ERROR, 'SettingCapsule[%s] error in loader function call: %s', label, error)

def default_on_use_default(label, *args, **kwargs):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] use the default setting', label)
