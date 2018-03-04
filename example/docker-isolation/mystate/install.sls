mystate-motd:
  file.managed:
    - name: /etc/motd
    - contents: |
        Hello salt test world
        {{ salt['pillar.get']('motd') }}

