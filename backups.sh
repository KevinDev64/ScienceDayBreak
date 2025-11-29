#!/bin/bash

find backups/ -name "*.tar.gz" -mtime +14 -delete
tar -czvf backups/"$(date)".tar.gz .
