"""Python package for using the Airship API"""
import logging

from .automation import Automation, Pipeline
from .common import AirshipFailure, Unauthorized
from .core import Airship
from .custom_events import CustomEvent
from .devices import (
    APIDList,
    Attribute,
    AttributeResponse,
    AttributeList,
    ChannelInfo,
    ChannelList,
    ChannelTags,
    ChannelUninstall,
    DeviceInfo,
    DeviceTokenList,
    Email,
    EmailAttachment,
    EmailTags,
    KeywordInteraction,
    ModifyAttributes,
    NamedUser,
    NamedUserList,
    NamedUserTags,
    OpenChannel,
    OpenChannelTags,
    Segment,
    SegmentList,
    Sms,
    SmsCustomResponse,
    StaticList,
    StaticLists,
    SubscriptionList,
)
from .experiments import ABTest, Experiment, Variant
from .push import (
    CreateAndSendPush,
    Push,
    ScheduledList,
    ScheduledPush,
    Template,
    TemplateList,
    TemplatePush,
    actions,
    alias,
    all_,
    amazon,
    amazon_channel,
    and_,
    android,
    android_channel,
    apid,
    best_time,
    campaigns,
    channel,
    date_attribute,
    device_token,
    device_types,
    email,
    in_app,
    interactive,
    ios,
    ios_channel,
    local_scheduled_time,
    localization,
    merge_data,
    message,
    mms,
    named_user,
    not_,
    notification,
    number_attribute,
    open_channel,
    open_platform,
    options,
    or_,
    public_notification,
    recurring_schedule,
    schedule_exclusion,
    static_list,
    subscription_list,
    scheduled_time,
    segment,
    sms,
    sms_id,
    sms_sender,
    style,
    tag,
    tag_group,
    text_attribute,
    wearable,
    web,
    wns,
    wns_payload,
)
from .reports import (
    AppOpensList,
    CustomEventsList,
    DevicesReport,
    ExperimentReport,
    IndividualResponseStats,
    OptInList,
    OptOutList,
    PushList,
    ResponseList,
    ResponseReportList,
    TimeInAppList,
    WebResponseReport,
)

__all__ = [
    Airship,
    AirshipFailure,
    Unauthorized,
    all_,
    Push,
    ScheduledPush,
    TemplatePush,
    ios_channel,
    android_channel,
    amazon_channel,
    channel,
    open_channel,
    device_token,
    apid,
    wns,
    tag,
    tag_group,
    alias,
    segment,
    sms_id,
    sms_sender,
    mms,
    and_,
    or_,
    not_,
    notification,
    ios,
    android,
    amazon,
    web,
    wns_payload,
    open_platform,
    message,
    in_app,
    options,
    campaigns,
    actions,
    interactive,
    device_types,
    scheduled_time,
    local_scheduled_time,
    sms,
    email,
    wearable,
    public_notification,
    style,
    best_time,
    named_user,
    merge_data,
    recurring_schedule,
    schedule_exclusion,
    static_list,
    subscription_list,
    localization,
    ChannelList,
    ChannelInfo,
    OpenChannel,
    Sms,
    DeviceTokenList,
    APIDList,
    DeviceInfo,
    Segment,
    SegmentList,
    ChannelUninstall,
    NamedUser,
    NamedUserList,
    NamedUserTags,
    IndividualResponseStats,
    ResponseList,
    DevicesReport,
    OptInList,
    OptOutList,
    PushList,
    ResponseReportList,
    AppOpensList,
    TimeInAppList,
    CustomEventsList,
    StaticList,
    StaticLists,
    Template,
    TemplateList,
    ScheduledList,
    Automation,
    Pipeline,
    Email,
    EmailTags,
    EmailAttachment,
    CreateAndSendPush,
    date_attribute,
    text_attribute,
    number_attribute,
    ChannelTags,
    OpenChannelTags,
    Attribute,
    AttributeResponse,
    AttributeList,
    ModifyAttributes,
    WebResponseReport,
    ExperimentReport,
    KeywordInteraction,
    SubscriptionList,
    CustomEvent,
]


logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
