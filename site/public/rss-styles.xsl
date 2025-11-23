<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:atom="http://www.w3.org/2005/Atom"
                xmlns:dc="http://purl.org/dc/elements/1.1/">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
      <head>
        <title><xsl:value-of select="/rss/channel/title"/> (RSS Feed)</title>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
          body {
            font-family: Georgia, Cambria, "Times New Roman", Times, serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
            color: #333;
            background-color: #fdfdfd;
          }
          header {
            border-bottom: 2px solid #eaeaea;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
          }
          h1 { margin-bottom: 0.5rem; }
          .subtitle { color: #666; font-style: italic; }
          .item {
            margin-bottom: 2.5rem;
            padding: 1.5rem;
            background: #fff;
            border: 1px solid #eee;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
          }
          .item h2 { margin-top: 0; font-size: 1.4rem; }
          .item h2 a { text-decoration: none; color: #2c3e50; }
          .item h2 a:hover { text-decoration: underline; color: #d35400; }
          .meta { font-size: 0.9rem; color: #888; margin-bottom: 1rem; display: block; }
        </style>
      </head>
      <body>
        <header>
          <h1><xsl:value-of select="/rss/channel/title"/></h1>
          <p class="subtitle"><xsl:value-of select="/rss/channel/description"/></p>
          <p><strong>This is an RSS feed.</strong> Subscribe by copying the URL into your news reader.</p>
        </header>
        <xsl:for-each select="/rss/channel/item">
          <div class="item">
            <h2>
              <a href="{link}" target="_blank">
                <xsl:value-of select="title"/>
              </a>
            </h2>
            <small class="meta">Published: <xsl:value-of select="pubDate"/></small>
            <p><xsl:value-of select="description" disable-output-escaping="yes"/></p>
          </div>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>