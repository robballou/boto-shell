"""
Simple shell for boto library

"""

import cmd
from boto.ec2.connection import EC2Connection
import os
import sys
from route53 import Route53Shell

class BotoShell(cmd.Cmd):
    line = "==========================================="
    instance_output = ""
    zone_output = "[%(Count)3d] Name:\t%(Name)s\n      ID:\t%(Id)s"
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'boto > '
        
        self.amazon_access_key_id = None
        self.amazon_secret_key = None
        
        self.subshell = None
        if len(sys.argv) == 2:
            if sys.argv[1] == 'route53': 
                self.subshell = Route53Shell(self)
                self.prompt = 'route53 > '
        if os.environ.has_key('AMAZON_ACCESS_KEY_ID'):
            self.amazon_access_key_id = os.environ['AMAZON_ACCESS_KEY_ID']
        if os.environ.has_key('AMAZON_SECRET_KEY'):
            self.amazon_secret_key = os.environ['AMAZON_SECRET_KEY']
    
    def default(self, line):
        if line == 'EOF':
            sys.stdout.write("\n")
            return True
        line_parts = line.split(' ')
        if not self.subshell:
            if line_parts[0] == "route53":
                self.subshell = Route53Shell(self)
                self.prompt = "route53 > "
                if len(line_parts) > 1:
                    method = "do_%s" % line_parts[1]
                    try:
                        func = getattr(self.subshell, method)
                        return func(' '.join(line_parts[1:]))
                    except AttributeError, e:
                        pass
                else:
                    return
            return cmd.Cmd.default(self, line)
        
        # check if the method exists within this class
        method = "do_%s" % (line_parts[0])
        try:
            func = getattr(self.subshell, method)
            if len(line_parts) > 1:
                return func(' '.join(line_parts[1:]))
            return func("")
        except AttributeError, e:
            print "%s" % e
        
        method = "do_%s_%s" % (self.subshell, line_parts[0])
        try:
            func = getattr(self, method)
            return func(line)
        except AttributeError, e:
            return cmd.Cmd.default(self, line)
    
    def do_access_key(self, access_key):
        """Set the authentication access key id"""
        self.amazon_access_key_id = access_key
    
    def do_auth(self, line):
        print "%s\n%s" % (self.amazon_access_key_id, self.amazon_secret_key)
    
    def do_ec2(self, line):
        self.subshell = "ec2"
        self.prompt = "ec2 > "
    
    def do_ec2_instances(self, line):
        """
        List all EC2 instances for this account
        """
        if not self.amazon_access_key_id or not self.amazon_secret_key:
            print "Authentication variables are not set."
            return
        
        conn = EC2Connection(self.amazon_access_key_id, self.amazon_secret_key)
        instances = conn.get_all_instances()
        print BotoShell.line
        for instance in instances:
            if len(instance.instances) == 1:
                self.print_instance(instance.instances[0])
                print BotoShell.line
    
    def do_ec2_snapshots(self, line):
        """List all snapshots for this account"""
        if not self.amazon_access_key_id or not self.amazon_secret_key:
            print "Authentication variables are not set."
            return
        
        conn = EC2Connection(self.amazon_access_key_id, self.amazon_secret_key)
        snapshots = conn.get_all_snapshots(owner='self')
        print BotoShell.line
        for snapshot in snapshots:
            print snapshot.__dict__
    
    def do_exit(self, line):
        return True
    
    def do_quit(self, line):
        return True
    
    def do_secret_key(self, secret_key):
        """Set the authentication secret key"""
        self.amazon_secret_key = secret_key
    
    def print_instance(self, instance):
        for key in instance.__dict__:
            print "%s: %s" % (key, getattr(instance, key))
