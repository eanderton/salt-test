{% load_yaml as testconfig %}

pillar:
  motd: pillar data

grains: {}

assert:
  passed: 2
  changed: 2
  failed: 0

{% endload %}

include:
  - mystate.install

test-bats:
  cmd.script:
    - source: salt://tests/install.bats
