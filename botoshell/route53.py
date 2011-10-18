import re

from boto.route53.connection import Route53Connection
from boto.route53.record import ResourceRecordSets, Record

class Route53Shell(object):
    def __init__(self, parent):
        self.shell = parent
        self.zone = None
    
    def do_add(self, line):
        """
        Add a new record
        """
        parts = line.split(' ')
        count = len(parts)
        if count == 0 and not self.zone:
            print "Zone not selected. Either pass a zone ID or set it with the zone command"
            return
        
        (record_name, record_type, record_ttl, record_value) = self.parse_change_command(parts)
        
        print "Create:\n\tName:\t%(name)s\n\tType:\t%(type)s\n\tTTL:\t%(ttl)d\n\tValue:\t%(value)s" % dict(
            name=record_name, type=record_type, ttl=record_ttl, value=record_value)
        
        conn = Route53Connection(self.shell.amazon_access_key_id, self.shell.amazon_secret_key)
        r = ResourceRecordSets(conn, self.zone)
        r.add_change('CREATE', record_name, record_type, record_ttl)
        if record_value:
            r.changes[0][1].add_value(record_value)
        change = conn.change_rrsets(self.zone, r.to_xml())
        print change
    
    def do_change(self, line):
        if not self.shell.amazon_access_key_id or not self.shell.amazon_secret_key:
            print "Authentication variables are not set."
            return

        parts = line.split(' ')
        count = len(parts)
        if count == 1 and not self.zone:
            print "Zone not selected. Either pass a zone ID or set it with the zone command"
            return
        
        (record_name, record_type, record_ttl, record_value) = self.parse_change_command(parts)
        
        conn = Route53Connection(self.shell.amazon_access_key_id, self.shell.amazon_secret_key)
        records = conn.get_all_rrsets(self.zone)
        this_record = None
        for record in records:
            if record.name == record_name or record.name == "%s." % record_name:
                this_record = record
                break
        
        print "Current:\n\tName:\t%(name)s\n\tType:\t%(type)s\n\tTTL:\t%(ttl)s\n\tValue:\t%(value)s" % dict(
            name=this_record.name, type=this_record.type, ttl=this_record.ttl, value=this_record.resource_records)
        
        print "New:\n\tName:\t%(name)s\n\tType:\t%(type)s\n\tTTL:\t%(ttl)d\n\tValue:\t%(value)s" % dict(
            name=record_name, type=record_type, ttl=record_ttl, value=record_value)
        
        r = ResourceRecordSets(conn, self.zone)
        r.add_change('DELETE', record_name, record_type, record_ttl)
        for value in this_record.resource_records:
            r.changes[0][1].add_value(value)
        r.add_change('CREATE', record_name, record_type, record_ttl)
        if record_value:
            r.changes[1][1].add_value(record_value)
        # print r.to_xml()
        change = conn.change_rrsets(self.zone, r.to_xml())
        print change
    
    def do_delete(self, line):
        if not self.shell.amazon_access_key_id or not self.shell.amazon_secret_key:
            print "Authentication variables are not set."
            return

        parts = line.split(' ')
        count = len(parts)
        if count == 1 and not self.zone:
            print "Zone not selected. Either pass a zone ID or set it with the zone command"
            return
        
        (record_name, record_type, record_ttl, record_value) = self.parse_change_command(parts)
        print "Delete:\n\tName:\t%(name)s\n\tType:\t%(type)s\n\tTTL:\t%(ttl)d\n\tValue:\t%(value)s" % dict(
            name=record_name, type=record_type, ttl=record_ttl, value=record_value)
        conn = Route53Connection(self.shell.amazon_access_key_id, self.shell.amazon_secret_key)
        r = ResourceRecordSets(conn, self.zone)
        r.add_change('DELETE', record_name, record_type, record_ttl)
        if record_value:
            r.changes[0][1].add_value(record_value)
        change = conn.change_rrsets(self.zone, r.to_xml())
        print change
    
    def do_list(self, line):
        """
        List all record sets in this zone
        """
        if not self.shell.amazon_access_key_id or not self.shell.amazon_secret_key:
            print "Authentication variables are not set."
            return
        
        parts = line.split(' ')
        if len(parts) == 0 and not self.zone:
            print "Zone not selected. Either pass a zone ID or set it with the zone command"
            return

        zone = self.zone
        if len(parts) == 1 and parts[0].strip() != "":
            zone = parts[0]
        elif not zone:
            print "Zone not selected. Either pass a zone ID or set it with the zone command"
            return
        
        print self.shell.line
        print "Zones for %s" % zone
        print self.shell.line
        
        conn = Route53Connection(self.shell.amazon_access_key_id, self.shell.amazon_secret_key)
        records = conn.get_all_rrsets(zone)
        for record in records:
            print "Name:\t%s" % record.name
            print "Type:\t%s" % record.type
            print "TTL:\t%s" % record.ttl
            for r in record.resource_records:
                print "\t- %s" % r
            print ""
    
    def do_zone(self, line):
        """
        Set the zone for any further method calls
        """
        parts = line.split(' ')
        if len(parts) > 1:
            print "Too many arguments: %s" % parts
            return
        
        if len(parts) == 1 and parts[0] == "":
            print self.zone
            return
        
        if re.match(r'^\d+$', line):
            # the line is numeric, so they are likely selecting a zone from the list of zones
            conn = Route53Connection(self.shell.amazon_access_key_id, self.shell.amazon_secret_key)
            zones = conn.get_all_hosted_zones()
            selected_zone = int(line)
            if len(zones['ListHostedZonesResponse']['HostedZones']) >= selected_zone:
                zone = selected_zone - 1
                line = zones['ListHostedZonesResponse']['HostedZones'][zone]['Id'].replace("/hostedzone/", "")
            else:
                print "Invalid zone"
                return
        
        self.zone = line
    
    def do_zones(self, line):
        """
        List the zones for this account
        """
        if not self.shell.amazon_access_key_id or not self.shell.amazon_secret_key:
            print "Authentication variables are not set."
            return
        
        conn = Route53Connection(self.shell.amazon_access_key_id, self.shell.amazon_secret_key)
        zones = conn.get_all_hosted_zones()
        print self.shell.line
        count = 1
        for zone in zones['ListHostedZonesResponse']['HostedZones']:
            zone['Id'] = zone['Id'].replace('/hostedzone/', '')
            zone['Count'] = count
            print self.shell.zone_output % zone
            print self.shell.line
            count += 1
    
    def parse_change_command(self, parts):
        count = len(parts)
        options = dict(
            record_type = 'A',
            record_ttl = 7200
        )
        
        # command can be:
        #   name
        #   zone name value
        #   zone name type value
        #   zone name type ttl value
        #   name value
        #   name type value
        #   name type ttl value
        record_name = None
        record_type = options['record_type']
        record_ttl = options['record_ttl']
        record_value = None
        
        if count == 1 and self.zone:
            record_name = parts[0]
        elif count == 2 and self.zone:
            # name value
            record_name = parts[0]
            record_value = parts[1]
        elif count == 3 and not self.zone:
            # zone name value
            self.zone = parts[0]
            record_name = parts[1]
            record_value = parts[2]
        elif count == 3 and self.zone:
            # name type value
            record_name = parts[0]
            record_type = parts[1]
            record_value = parts[2]
        elif count == 4 and self.zone:
            # name type ttl value
            record_name = parts[0]
            record_type = parts[1]
            record_ttl = parts[2]
            record_value = parts[3]
        elif count == 4 and not self.zone:
            # zone name type value
            self.zone = parts[0]
            record_name = parts[1]
            record_type = parts[2]
            record_value = parts[3]
        elif count == 5 and not self.zone:
            # zone name type value
            self.zone = parts[0]
            record_name = parts[1]
            record_type = parts[2]
            record_ttl = parts[3]
            record_value = parts[4]
        
        return (record_name, record_type, record_ttl, record_value)
    