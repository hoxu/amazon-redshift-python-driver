import logging
import typing

from redshift_connector import plugin
from redshift_connector.config import DEFAULT_PROTOCOL_VERSION
from redshift_connector.core import BINARY, Connection, Cursor
from redshift_connector.error import (
    ArrayContentNotHomogenousError,
    ArrayContentNotSupportedError,
    ArrayDimensionsNotConsistentError,
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Warning,
)
from redshift_connector.iam_helper import IamHelper
from redshift_connector.objects import (
    Binary,
    Date,
    DateFromTicks,
    Time,
    TimeFromTicks,
    Timestamp,
    TimestampFromTicks,
)
from redshift_connector.pg_types import (
    PGEnum,
    PGJson,
    PGJsonb,
    PGText,
    PGTsvector,
    PGVarchar,
)
from redshift_connector.redshift_property import RedshiftProperty
from redshift_connector.utils import (
    DriverInfo,
    make_divider_block,
    mask_secure_info_in_props,
)
from redshift_connector.utils.type_utils import (
    ABSTIME,
    BIGINT,
    BIGINTEGER,
    BOOLEAN,
    BOOLEAN_ARRAY,
    BYTES,
    CHAR,
    CHAR_ARRAY,
    DATE,
    DATETIME,
    DECIMAL,
    DECIMAL_ARRAY,
    FLOAT,
    FLOAT_ARRAY,
    GEOMETRY,
    GEOMETRYHEX,
    INET,
    INT2VECTOR,
    INTEGER,
    INTEGER_ARRAY,
    INTERVAL,
    JSON,
    JSONB,
    MACADDR,
    NAME,
    NAME_ARRAY,
    NULLTYPE,
    NUMBER,
    OID,
    ROWID,
    SMALLINT,
    STRING,
    SUPER,
    TEXT,
    TEXT_ARRAY,
    TIME,
    TIMESTAMP,
    TIMESTAMPTZ,
    TIMETZ,
    UNKNOWN,
    UUID_TYPE,
    VARBYTE,
    VARCHAR,
    VARCHAR_ARRAY,
    XID,
)

from .version import __version__

logging.getLogger(__name__).addHandler(logging.NullHandler())
_logger: logging.Logger = logging.getLogger(__name__)

# Copyright (c) 2007-2009, Mathieu Fenniak
# Copyright (c) The Contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# * The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__author__ = "Mathieu Fenniak"


def connect(
    user: typing.Optional[str] = None,
    database: typing.Optional[str] = None,
    password: typing.Optional[str] = None,
    port: typing.Optional[int] = None,
    host: typing.Optional[str] = None,
    source_address: typing.Optional[str] = None,
    unix_sock: typing.Optional[str] = None,
    ssl: typing.Optional[bool] = None,
    sslmode: typing.Optional[str] = None,
    timeout: typing.Optional[int] = None,
    max_prepared_statements: typing.Optional[int] = None,
    tcp_keepalive: typing.Optional[bool] = None,
    application_name: typing.Optional[str] = None,
    replication: typing.Optional[str] = None,
    idp_host: typing.Optional[str] = None,
    db_user: typing.Optional[str] = None,
    app_id: typing.Optional[str] = None,
    app_name: typing.Optional[str] = None,
    preferred_role: typing.Optional[str] = None,
    principal_arn: typing.Optional[str] = None,
    access_key_id: typing.Optional[str] = None,
    secret_access_key: typing.Optional[str] = None,
    session_token: typing.Optional[str] = None,
    profile: typing.Optional[str] = None,
    credentials_provider: typing.Optional[str] = None,
    region: typing.Optional[str] = None,
    cluster_identifier: typing.Optional[str] = None,
    iam: typing.Optional[bool] = None,
    client_id: typing.Optional[str] = None,
    idp_tenant: typing.Optional[str] = None,
    client_secret: typing.Optional[str] = None,
    partner_sp_id: typing.Optional[str] = None,
    idp_response_timeout: typing.Optional[int] = None,
    listen_port: typing.Optional[int] = None,
    login_url: typing.Optional[str] = None,
    auto_create: typing.Optional[bool] = None,
    db_groups: typing.Optional[typing.List[str]] = None,
    force_lowercase: typing.Optional[bool] = None,
    allow_db_user_override: typing.Optional[bool] = None,
    client_protocol_version: typing.Optional[int] = None,
    database_metadata_current_db_only: typing.Optional[bool] = None,
    ssl_insecure: typing.Optional[bool] = None,
    web_identity_token: typing.Optional[str] = None,
    role_session_name: typing.Optional[str] = None,
    role_arn: typing.Optional[str] = None,
    iam_disable_cache: typing.Optional[bool] = None,
    auth_profile: typing.Optional[str] = None,
    endpoint_url: typing.Optional[str] = None,
) -> Connection:
    """
    Establishes a :class:`Connection` to an Amazon Redshift cluster. This function validates user input, optionally authenticates using an identity provider plugin, then constructs a :class:`Connection` object.

    Parameters
    ----------
    user : Optional[str]
        The username to use for authentication with the Amazon Redshift cluster.
    password : Optional[str]
        The password to use for authentication with the Amazon Redshift cluster.
    database : Optional[str]
        The name of the database instance to connect to.
    host : Optional[str]
        The hostname of the Amazon Redshift cluster.
    port : Optional[int]
        The port number of the Amazon Redshift cluster. Default value is 5439.
    source_address : typing.Optional[str]
    unix_sock : Optional[str]
    ssl : Optional[bool]
        Is SSL enabled. Default value is ``True``. SSL must be enabled when authenticating using IAM.
    sslmode : Optional[str]
        The security of the connection to the Amazon Redshift cluster. 'verify-ca' and 'verify-full' are supported.
    timeout : Optional[int]
        The number of seconds before the connection to the server will timeout. By default there is no timeout.
    max_prepared_statements : Optional[int]
    tcp_keepalive : Optional[bool]
        Is `TCP keepalive <https://en.wikipedia.org/wiki/Keepalive#TCP_keepalive>`_ used. The default value is ``True``.
    application_name : Optional[str]
        Sets the application name. The default value is None.
    replication : Optional[str]
        Used to run in `streaming replication mode <https://www.postgresql.org/docs/12/protocol-replication.html>`_.
    idp_host : Optional[str]
        The hostname of the IdP.
    db_user : Optional[str]
        The user ID to use with Amazon Redshift
    app_id : Optional[str]
    app_name : Optional[str]
        The name of the identity provider (IdP) application used for authentication.
    preferred_role : Optional[str]
        The IAM role preferred for the current connection.
    principal_arn : Optional[str]
        The ARN of the IAM entity (user or role) for which you are generating a policy.
    credentials_provider : Optional[str]
        The class name of the IdP that will be used for authenticating with the Amazon Redshift cluster.
    region : Optional[str]
        The AWS region where the Amazon Redshift cluster is located.
    cluster_identifier : Optional[str]
        The cluster identifier of the Amazon Redshift cluster.
    iam : Optional[bool]
        If IAM authentication is enabled. Default value is False. IAM must be True when authenticating using an IdP.
    client_id : Optional[str]
        The client id from Azure IdP.
    idp_tenant : Optional[str]
        The IdP tenant.
    client_secret : Optional[str]
        The client secret from Azure IdP.
    partner_sp_id : Optional[str]
        The Partner SP Id used for authentication with Ping.
    idp_response_timeout : Optional[int]
        The timeout for retrieving SAML assertion from IdP. Default value is `120`.
    listen_port : Optional[int]
        The listen port the IdP will send the SAML assertion to. Default value is `7890`.
    login_url : Optional[str]
        The SSO url for the IdP.
    auto_create : Optional[bool]
        Indicates whether the user should be created if they do not exist. Default value is `False`.
    db_groups : Optional[str]
        A comma-separated list of existing database group names that the `db_user` joins for the current session.
    force_lowercase : Optional[bool]
    allow_db_user_override : Optional[bool]
        Specifies if the driver uses the `db_user` value from the SAML assertion. TDefault value is `False`.
    client_protocol_version : Optional[int]
         The requested server protocol version. The default value is 2 representing `BINARY`. If the requested server protocol cannot be satisfied a warning will be displayed to the user and the driver will default to the highest supported protocol. See `ClientProtocolVersion` for more details.
    database_metadata_current_db_only : Optional[bool]
        Is `datashare <https://docs.aws.amazon.com/redshift/latest/dg/datashare-overview.html>`_ disabled. Default value is True, implying datasharing will not be used.
    ssl_insecure : Optional[bool]
        Specifies if IdP host's server certificate will be verified. Default value is True
    web_identity_token: Optional[str]
        A web identity token used for authentication with JWT.
    role_session_name: Optional[str]
        An identifier for the assumed role session used for authentication with JWT.
    role_arn: Optional[str]
        The role ARN used for authentication with JWT. This parameter is required when using a JWTCredentialsProvider.
    iam_disable_cache: Optional[bool]
        This option specifies whether the IAM credentials are cached. By default caching is enabled.
    auth_profile: Optional[str]
        The name of an Amazon Redshift Authentication profile having connection properties as JSON. See :class:RedshiftProperty to learn how connection properties should be named.
    endpoint_url: Optional[str]
        The Amazon Redshift endpoint url. This option is only used by AWS internal teams.
    Returns
    -------
    A Connection object associated with the specified Amazon Redshift cluster: :class:`Connection`
    """
    info: RedshiftProperty = RedshiftProperty()
    info.put("access_key_id", access_key_id)
    info.put("allow_db_user_override", allow_db_user_override)
    info.put("app_id", app_id)
    info.put("app_name", app_name)
    info.put("application_name", application_name)
    info.put("auth_profile", auth_profile)
    info.put("auto_create", auto_create)
    info.put("client_id", client_id)
    info.put("client_protocol_version", client_protocol_version)
    info.put("client_secret", client_secret)
    info.put("cluster_identifier", cluster_identifier)
    info.put("credentials_provider", credentials_provider)
    info.put("database_metadata_current_db_only", database_metadata_current_db_only)
    info.put("db_groups", db_groups)
    info.put("db_name", database)
    info.put("db_user", db_user)
    info.put("endpoint_url", endpoint_url)
    info.put("force_lowercase", force_lowercase)
    info.put("host", host)
    info.put("iam", iam)
    info.put("iam_disable_cache", iam_disable_cache)
    info.put("idp_host", idp_host)
    info.put("idp_response_timeout", idp_response_timeout)
    info.put("idp_tenant", idp_tenant)
    info.put("listen_port", listen_port)
    info.put("login_url", login_url)
    info.put("max_prepared_statements", max_prepared_statements)
    info.put("partner_sp_id", partner_sp_id)
    info.put("password", password)
    info.put("port", port)
    info.put("preferred_role", preferred_role)
    info.put("principal", principal_arn)
    info.put("profile", profile)
    info.put("region", region)
    info.put("replication", replication)
    info.put("role_arn", role_arn)
    info.put("role_session_name", role_session_name)
    info.put("secret_access_key", secret_access_key)
    info.put("session_token", session_token)
    info.put("source_address", source_address)
    info.put("ssl", ssl)
    info.put("ssl_insecure", ssl_insecure)
    info.put("sslmode", sslmode)
    info.put("tcp_keepalive", tcp_keepalive)
    info.put("timeout", timeout)
    info.put("unix_sock", unix_sock)
    info.put("user_name", user)
    info.put("web_identity_token", web_identity_token)

    _logger.debug(make_divider_block())
    _logger.debug("User provided connection arguments")
    _logger.debug(make_divider_block())
    _logger.debug(mask_secure_info_in_props(info).__str__())
    _logger.debug(make_divider_block())

    IamHelper.set_iam_properties(info)

    _logger.debug(make_divider_block())
    _logger.debug("Connection arguments following validation and IAM auth (if applicable)")
    _logger.debug(make_divider_block())
    _logger.debug(mask_secure_info_in_props(info).__str__())
    _logger.debug(make_divider_block())

    return Connection(
        user=info.user_name,
        host=info.host,
        database=info.db_name,
        port=info.port,
        password=info.password,
        source_address=info.source_address,
        unix_sock=info.unix_sock,
        ssl=info.ssl,
        sslmode=info.sslmode,
        timeout=info.timeout,
        max_prepared_statements=info.max_prepared_statements,
        tcp_keepalive=info.tcp_keepalive,
        application_name=info.application_name,
        replication=info.replication,
        client_protocol_version=info.client_protocol_version,
        database_metadata_current_db_only=info.database_metadata_current_db_only,
        credentials_provider=info.credentials_provider,
    )


apilevel: str = "2.0"
"""The DBAPI level supported, currently "2.0".

This property is part of the `DBAPI 2.0 specification
<http://www.python.org/dev/peps/pep-0249/>`_.
"""

threadsafety: int = 1
"""Integer constant stating the level of thread safety the DBAPI interface
supports. This DBAPI module supports sharing of the module only. Connections
and cursors my not be shared between threads.

This property is part of the `DBAPI 2.0 specification
<http://www.python.org/dev/peps/pep-0249/>`_.
"""

paramstyle: str = "format"
"""
String property stating the type of parameter marker formatting expected by the interface; This value defaults to "format", in which parameters are marked in this format "WHERE name=%s"
"""

__all__: typing.Any = [
    "Warning",
    "DataError",
    "DatabaseError",
    "connect",
    "InterfaceError",
    "ProgrammingError",
    "Error",
    "OperationalError",
    "IntegrityError",
    "InternalError",
    "NotSupportedError",
    "ArrayContentNotHomogenousError",
    "ArrayDimensionsNotConsistentError",
    "ArrayContentNotSupportedError",
    "Connection",
    "Cursor",
    "Binary",
    "Date",
    "DateFromTicks",
    "Time",
    "TimeFromTicks",
    "Timestamp",
    "TimestampFromTicks",
    "BINARY",
    "PGEnum",
    "PGJson",
    "PGJsonb",
    "PGTsvector",
    "PGText",
    "PGVarchar",
    "__version__",
    "ABSTIME",
    "BIGINT",
    "BIGINTEGER",
    "BOOLEAN",
    "BOOLEAN_ARRAY",
    "BYTES",
    "CHAR",
    "CHAR_ARRAY",
    "DATE",
    "DATETIME",
    "DECIMAL",
    "DECIMAL_ARRAY",
    "FLOAT",
    "FLOAT_ARRAY",
    "GEOMETRY",
    "GEOMETRYHEX",
    "INET",
    "INT2VECTOR",
    "INTEGER",
    "INTEGER_ARRAY",
    "INTERVAL",
    "JSON",
    "JSONB",
    "MACADDR",
    "NAME",
    "NAME_ARRAY",
    "NULLTYPE",
    "NUMBER",
    "OID",
    "ROWID",
    "STRING",
    "SMALLINT",
    "SUPER",
    "TEXT",
    "TEXT_ARRAY",
    "TIME",
    "TIMESTAMP",
    "TIMESTAMPTZ",
    "TIMETZ",
    "UNKNOWN",
    "UUID_TYPE",
    "VARCHAR",
    "VARCHAR_ARRAY",
    "XID",
]
