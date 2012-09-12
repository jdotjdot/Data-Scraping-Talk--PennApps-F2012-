# This is an example of a scraper I wrote for the Craigslist
# URLs in the URLS array.
# It goes to each listing on a page of listings, goes to each
    # listing page and grabs a number of items of information,
    # ignoring HTML comments and grabbing a list of images
    # as a list.  This is then all saved to a Django model.

# Copyright J.J. Fliegelman 2012, All Rights Reserved
# May not be shared or reproduced in any fashion without express written consent of copyright holder


import requests, sys, datetime, re, pprint
from bs4 import BeautifulSoup
#from models import listing, imagelist


URLS = ['http://dallas.craigslist.org/vga/',
        'http://dallas.craigslist.org/ele/',
        'http://dallas.craigslist.org/pts/']

def convert_time(string):
    f = re.search(r'(?P<year>\d{4})\-(?P<month>\d{2})\-(?P<day>\d{2}), +(?P<hour>\d{1,2}):(?P<minute>\d{1,2})(?P<am>[AP]M)(?= CDT)',
                     string)

    hour = int(f.group('hour'))
    if hour != 12:
        if f.group('am') == 'PM':
            hour += 12
    else:
        if f.group('am') == 'AM':
            hour = 0
        else:
            hour = 12
    

    return datetime.datetime(int(f.group('year')),
                             int(f.group('month')),
                             int(f.group('day')),
                             hour,
                             int(f.group('minute')))
                             

def normalize_phone(string):
    '''This normalizes varying forms of phone numbers into a single
    form with only numerals and no separators.'''


    string = re.sub(r'[^\da-zA-Z]', '', string)

    if re.search('[a-zA-Z]', string):
        numdict = {}
        convlist = (('abc', 2), ('def', 3), ('ghi', 4), ('jkl', 5),
            ('mno', 6), ('pqrs', 7), ('tuv', 8), ('wxyz', 9))
        for letters, num in convlist:
            for letter in letters:
                numdict[letter] = str(num)

    string = map(lambda x: x if x.isdigit() else numdict[x.lower()], string)
    
    return ''.join(string)

def get_page(url, session=None, soup=True):
    if not session:
       session = requests.session(config = {'verbose': sys.stderr})

    text = session.get(url).text

    if soup:
        return BeautifulSoup(text)
    else:
        return text

def get_listing_urls(soup):
    '''This takes in a BeautifulSoup object of a Craigslist
        listings page and returns a list of all of the listing urls.'''

    temp = soup.find_all('p', 'row')
    return [x.a.attrs['href'] for x in temp]


def scrape_listing(url, separate_images=True):

    soup = get_page(url)
    out = {}

    #url, title, body, posting_time, imglist, phone, email, scraping_time
    
    out['url'] = url
    # print soup.find(lambda tag: 'Date:' in tag.text and \
                        # (tag.next_sibling.name == 'br' or \
                        # (tag.next_sibling.next_sibling.name == 'br')))
    
    out['title'] = soup.h2.text.strip()
    body = soup.find(id='userbody').text.strip()
    out['body'] = re.sub(r'<!--.*?-->', '', body)
    
    out['posting_time'] = convert_time(soup.find('span', 'postingdate').text.strip())

        
    out['imglist'] = re.findall(r'http://images.craigslist.org/[a-zA-Z0-9_]+?.jpg', body)
    if not out['imglist']:
        out['imglist'] = []

    phone = re.compile(r'\(?(?P<area>214|469|972|817)\)?[.\-\s]?(?P<mid>\w{3})[.\-\s]?(?P<end>\w{4})')

    if any([x in out['body'] for x in ['214','469','972','817']]):
        try:
            extract = phone.search(out['body']).group(0)
        except AttributeError:
            out['phone'] = "Phone disguising used"
        else:
            out['phone'] = normalize_phone(extract)

    else:
        out['phone'] = ''
        
    print out['phone']

    try:
        out['email'] = soup.find(lambda tag: 'href' in tag.attrs and \
                             tag.attrs['href'].startswith('mailto:')).text
    except AttributeError:
        out['email'] = "None given"
    
    out['scraping_time'] = datetime.datetime.now()

    if separate_images:
        imglist = out['imglist']
        del out['imglist']
        return (out, imglist)
    else:
        return out


def main():
    for url in URLS:
        for x in get_listing_urls(get_page(url)):
            try:
                listobj, imglistobj = scrape_listing(x)
                
                # if not listing.objects.filter(url = listobj['url']):
                # listobj = listing(**listobj)
                # listobj.save()
                # for url in imglistobj:
                #     x = imagelist(img_url = url, listing = listobj)
                #     x.save()
                pprint.pprint(listobj)
                    
            except:
                print "The job for url %s failed." % url
                continue
            
if __name__ == '__main__':
    main()