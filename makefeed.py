import os
import re
import datetime
import PyRSS2Gen
import urllib.parse
import datetime

folder_path = "/Volumes/newshare/share/"  # Replace with the path to your folder
rss_file_path = "/Volumes/newshare/share/rss.xml"  # Replace with the path where you want to save the RSS file
rss_title = "Master Busa Library"
rss_link = "http://172.16.15.9:8888/"  # Replace with your website's URL
share_path = "/Volumes/newshare/share"

allowed_extensions = ['.mkv', '.avi', '.mp4']  # Allowed file extensions

print("Scanning files in %s" % folder_path)

items = []
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        extension = os.path.splitext(filename)[1].lower()
        if extension in allowed_extensions:

            # Extract the relative path from the file path
            relative_path = os.path.join(root, filename).replace(share_path, "")
            
            # Encode the path to ensure that it is safe for URLs
            encoded_path = urllib.parse.quote(relative_path)
            
            # Build the URL by joining the server address and encoded path
            url = urllib.parse.urljoin(rss_link, encoded_path)

            # Get the file's creation time
            created_time = os.path.getctime(os.path.join(root, filename))
            
            # Convert the creation time to UTC timezone
            utc_time = datetime.datetime.utcfromtimestamp(created_time)
            
            # Format the time in RFC822 format for the RSS feed
            pub_date = utc_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
            thumbnail_url = os.path.join(rss_link, f"{os.path.splitext(filename)[0]}-thumb.jpg".replace(" ", "\\ "))

            # Extract readable names
            match = re.search("^(.+)(S\d{2}E\d{2})|^(.+)(\d{4})|^(.+)(?<![\.mkv|\.avi\.mp4])", filename) 

            if match.group(1) != None:
                
                title = match.group(1).replace(".", " ").strip()                
                if match.group(2) != None:
                    episode = match.group(2).replace(".", " ").strip()
                    description = "<font size='5'><b>New episode:</b> %s<br><br><b>Filename:</b> %s<br><br> Download it from <a href='%s'>Master Busa</a></font>" % (episode, filename, url)

            elif match.group(3) != None:
                title = match.group(3).replace(".", " ").strip()
                description = "<font size='5'><b>Filename:</b> %s<br><br>Download it from <a href='%s'>Master Busa</a></font>" % (filename, url)
            
                if match.group(4) != None:
                    year = match.group(4)
                    description = "<font size='5'><b>Yes:</b> %s<br><br><b>Filename:</b> %s<br><br> Download it from <a href='%s'>Master Busa</a></font>" % (year, filename, url)

            else:
                title = filename
                description = "<font size='5'><b>Filename:</b> %s<br><br>Download it from <a href='%s'>Master Busa</a></font>" % (filename, url)

            # try:
            #     episode = match.group(2).replace(".", " ").strip()
            #     description = "<font size='5'><b>New episode:</b> %s<br><br><b>Filename:</b> %s<br><br> Download it  from <a href='%s'>Master Busa</a></font>" % (episode, filename, url)
            # except:
            #     description = "<font size='5'><b>Filename:</b> %s<br><br>Download it from <a href='%s'>Master Busa</a></font>" % (filename, url)

            # Create the RSS item
            item = PyRSS2Gen.RSSItem(
                title=title,
                link=url,
                description=description,
                pubDate=pub_date,
                enclosure=PyRSS2Gen.Enclosure(
                    url=thumbnail_url,
                    type=f"image/jpeg",
                    length=0,
                )
            )

            items.append(item)

# Sort the RSS items by date, with the most recent items on top
items.sort(key=lambda x: x.pubDate, reverse=True)

# Create the RSS feed
rss = PyRSS2Gen.RSS2(
    title=rss_title,
    link=rss_link,
    description=rss_title,
    lastBuildDate=datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
    items=items
)

try:
    # Write the RSS feed to a file
    rss.write_xml(open(rss_file_path, "w", encoding="utf-8"))

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

    print("Created RSS file at %s" % formatted_date)
except Exception as e:
    raise e
