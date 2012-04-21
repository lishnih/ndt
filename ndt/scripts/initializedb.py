#!/usr/bin/env python
# coding=utf-8

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ndt.models import (
    DBSession,
    Base,
    Group,
    User,
    Db,
    Option,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'db_users.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:

        user = User(
            name     = 'admin',
            password = 'admin',
            email    = 'admin@localhost'
        )
        DBSession.add(user)

        phase1_group = Group(
            name     = 'A94001',
            homedir  = 'D:/opt/home/a94001',
        )
        DBSession.add(phase1_group)

        phase2_group = Group(
            name     = u'A94001-2 очередь',
            homedir  = 'D:/opt/home/a94001-2',
        )
        DBSession.add(phase2_group)

        qc_user1 = User(
            name     = 'Oleg',
            password = '',
            email    = 'oleg@localhost'
        )
        DBSession.add(qc_user1)

        phase1_group.users.append(qc_user1)

        qc_user2 = User(
            name     = 'Stan',
            password = '',
            email    = 'stan@localhost'
        )
        DBSession.add(qc_user2)

        phase1_group.users.append(qc_user2)
        phase2_group.users.append(qc_user2)



if __name__ == '__main__':
    main(argv=['', ur'..\..\development.ini'])
