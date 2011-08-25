# A simple AWS shell

This is a simple shell for AWS using the great boto library. 

## Authentication

Just like boto itself, you can use the environment variables `AMAZON\_ACCESS\_KEY\_ID` and `AMAZON\_SECRET\_KEY` to set your account authentication. Or you can set/change the keys in boto-shell:

    boto > access_key [key]
    boto > secret_key [key]

## Subshells

To act on things like EC2 or Route53, you can either enter the "subshell" or enter the command directly. For instance:

    boto > route53 zones

Will enter the route53 subshell and run the `zones` command. Or:

    boto > route53
    route53 > 

## List Route53 zones

    boto > route53
    route53 > zones
    ...

## List records in a Route53 zone

    boto > route53 zones
    ...
    route53 > zone [id]
    route53 > list
    ...

# License

Boto Library Copyright (c) 2006-2011 Mitch Garnaat mitch@garnaat.com Copyright (c) 2010-2011, Eucalyptus Systems, Inc. All rights reserved.

Boto Shell Copyright (c) 2011 Rob Ballou

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.