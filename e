[4mDOCKER[24m(1)                                                            Docker User Manuals                                                           [4mDOCKER[24m(1)

[1mNAME[0m
       docker - Docker image and container command line interface

[1mSYNOPSIS[0m
       [1mdocker [22m[OPTIONS] COMMAND [ARG...]

       [1mdocker [22m[--help|-v|--version]

[1mDESCRIPTION[0m
       [1mdocker [22mis a client for interacting with the daemon (see [1mdockerd(8)[22m) through the CLI.

       The Docker CLI has over 30 commands. The commands are listed below and each has its own man page which explains usage and arguments.

       To see the man page for a command run [1mman docker [22m.

[1mOPTIONS[0m
       [1m--help[0m
         Print usage statement

       [1m--config[22m=""
         Specifies the location of the Docker client configuration files. The default is '~/.docker'.

       [1m-D[22m, [1m--debug[22m=[4mtrue[24m|[4mfalse[0m
         Enable debug mode. Default is false.

       [1m-H[22m, [1m--host[22m=[[4munix:///var/run/docker.sock[24m]: tcp://[host]:[port][path] to bind or unix://[/path/to/socket] to use.
         The socket(s) to bind to in daemon mode specified using one or more
         tcp://host:port/path, unix:///path/to/socket, fd://* or fd://socketfd.
         If the tcp port is not specified, then it will default to either [1m2375 [22mwhen
         [1m--tls [22mis off, or [1m2376 [22mwhen [1m--tls [22mis on, or [1m--tlsverify [22mis specified.

       [1m-l[22m, [1m--log-level[22m="[4mdebug[24m|[4minfo[24m|[4mwarn[24m|[4merror[24m|[4mfatal[24m"
         Set the logging level. Default is [1minfo[22m.

       [1m--tls[22m=[4mtrue[24m|[4mfalse[0m
         Use TLS; implied by --tlsverify. Default is false.

       [1m--tlscacert[22m=[4m~/.docker/ca.pem[0m
         Trust certs signed only by this CA.

       [1m--tlscert[22m=[4m~/.docker/cert.pem[0m
         Path to TLS certificate file.

       [1m--tlskey[22m=[4m~/.docker/key.pem[0m
         Path to TLS key file.

       [1m--tlsverify[22m=[4mtrue[24m|[4mfalse[0m
         Use TLS and verify the remote (daemon: verify client, client: verify daemon).
         Default is false.

       [1m-v[22m, [1m--version[22m=[4mtrue[24m|[4mfalse[0m
         Print version information and quit. Default is false.

[1mCOMMANDS[0m
       Use "docker help" or "docker --help" to get an overview of available commands.

[1mEXAMPLES[0m
       For specific client examples see the man page for the specific Docker command. For example:

       man docker-run

[1mHISTORY[0m
       April 2014, Originally compiled by William Henry (whenry at redhat dot com) based on docker.com source material and internal work.

Docker Community                                                         APRIL 2014                                                                [4mDOCKER[24m(1)
