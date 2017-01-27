#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='migrations', url='postgresql://tweetsql:tweetsql@127.0.0.1/tweetsql', debug='False')
