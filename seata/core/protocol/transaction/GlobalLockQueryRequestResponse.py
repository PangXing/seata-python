#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author jsbxyyx
# @since 1.0
from seata.core.model.BranchType import BranchType
from seata.core.protocol.MessageType import MessageType
from seata.core.protocol.MessageTypeAware import MessageTypeAware, ResultMessage
from seata.exception.TransactionExceptionCode import TransactionExceptionCode


class GlobalLockQueryRequest(MessageTypeAware):

    def __int__(self):
        self.xid = None
        self.branch_type = BranchType.AT
        self.resource_id = None
        self.lock_key = None
        self.application_data = None

    def get_type_code(self):
        return MessageType.TYPE_GLOBAL_LOCK_QUERY


class GlobalLockQueryResponse(ResultMessage, MessageTypeAware):

    def __init__(self):
        super(GlobalLockQueryResponse, self).__init__()
        self.lockable = False

        self.transaction_exception_code = TransactionExceptionCode.Unknown
        self.result_code = None
        self.msg = None

    def get_type_code(self):
        return MessageType.TYPE_GLOBAL_LOCK_QUERY_RESULT
