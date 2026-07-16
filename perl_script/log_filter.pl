#!/usr/bin/perl
# 过滤日志中的报错关键词
while(<STDIN>){
    print $_ if /error|fail|exception/i;
}

