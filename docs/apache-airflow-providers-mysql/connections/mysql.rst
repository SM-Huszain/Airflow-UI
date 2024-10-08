 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

 ..   http://www.apache.org/licenses/LICENSE-2.0

 .. Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.



.. _howto/connection:mysql:

MySQL Connection
================
The MySQL connection type provides connection to a MySQL database.

Configuring the Connection
--------------------------
Host (required)
    The host to connect to.

Schema (optional)
    Specify the schema name to be used in the database.

Login (required)
    Specify the user name to connect.

Password (required)
    Specify the password to connect.

Extra (optional)
    Specify the extra parameters (as json dictionary) that can be used in MySQL
    connection. Note that you can choose the client to connect to the database by setting the ``client`` extra field.

    For ``mysqlclient`` (default) the following extras are supported:

      * ``charset``: specify charset of the connection
      * ``cursor``: one of ``sscursor``, ``dictcursor``, ``ssdictcursor`` . Specifies cursor class to be
        used
      * ``unix_socket``: UNIX socket used instead of the default socket.
      * ``ssl``: Dictionary of SSL parameters that control connecting using SSL. Those
        parameters are server specific and should contain ``ca``, ``cert``, ``key``, ``capath``,
        ``cipher`` parameters. See
        `MySQLdb docs <https://mysqlclient.readthedocs.io/user_guide.html>`_ for details.
        Note that to be useful in URL notation, this parameter might also be
        a string where the SSL dictionary is a string-encoded JSON dictionary.

      Example "extras" field:

      .. code-block:: json

         {
            "charset": "utf8",
            "cursor": "sscursor",
            "unix_socket": "/var/socket",
            "ssl": {
              "cert": "/tmp/client-cert.pem",
              "ca": "/tmp/server-ca.pem",
              "key": "/tmp/client-key.pem"
            }
         }

      or

      .. code-block:: json

         {
            "charset": "utf8",
            "cursor": "sscursor",
            "unix_socket": "/var/socket",
            "ssl": "{\"cert\": \"/tmp/client-cert.pem\", \"ca\": \"/tmp/server-ca.pem\", \"key\": \"/tmp/client-key.pem\"}"
         }

      When specifying the connection as URI (in :envvar:`AIRFLOW_CONN_{CONN_ID}` variable) you should specify it
      following the standard syntax of DB connections - where extras are passed as parameters
      of the URI. Note that all components of the URI should be URL-encoded.

      For example:

      .. code-block:: bash

         export AIRFLOW_CONN_MYSQL_DEFAULT='mysql://mysql_user:XXXXXXXXXXXX@1.1.1.1:3306/mysqldb?ssl=%7B%22cert%22%3A+%22%2Ftmp%2Fclient-cert.pem%22%2C+%22ca%22%3A+%22%2Ftmp%2Fserver-ca.pem%22%2C+%22key%22%3A+%22%2Ftmp%2Fclient-key.pem%22%7D'

      .. note::
          If encounter UnicodeDecodeError while working with MySQL connection, check
          the charset defined is matched to the database charset.

    For ``mysql-connector-python`` no extras are supported:

In both cases, when you want to use ``LOAD DATA LOCAL INFILE`` SQL commands of MySQl, you need to create the
Hook with "local_infile" parameter set to True.
