#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author jsbxyyx
# @since 1.0
from seata.core.model.BranchType import BranchType
from seata.core.protocol.MessageType import MessageType
from seata.core.protocol.MessageTypeAware import MessageTypeAware, ResultMessage


class BranchRegisterRequest(MessageTypeAware):

    def __int__(self):
        self.xid = None
        self.branch_type = BranchType.AT
        self.resource_id = None
        self.lock_key = None
        self.application_data = None

    def get_type_code(self):
        return MessageType.TYPE_BRANCH_REGISTER


class BranchRegisterResponse(ResultMessage, MessageTypeAware):

    def __init__(self):
        self.branch_id = 0

        self.transaction_exception_code = None
        self.result_code = None
        self.msg = None

    def get_type_code(self):
        return MessageType.TYPE_BRANCH_REGISTER_RESULT
