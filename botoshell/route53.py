from boto.route53.connection import Route53Connection

class Route53Shell(object):
    def __init__(self, parent):
        self.shell = parent
        self.zone = None
    
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
        if len(parts) == 1 and parts[0] != "":
            zone = parts[0]
        
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
        for zone in zones['ListHostedZonesResponse']['HostedZones']:
            zone['Id'] = zone['Id'].replace('/hostedzone/', '')
            print self.shell.zone_output % zone
            print self.shell.line
    