#!/usr/bin/env bats

@test "test motd exists" {
  [ -f /etc/motd ]
}

@test "test motd content" {
  cat /etc/motd | grep 'Hello salt test world'
}

@test "test motd pillar content" {
  cat /etc/motd | grep 'pillar data'
}
