#!/usr/bin/env python3
"""
Generate the city landing pages under locations/<slug>/index.html.

Andreina's site has no build system, so this is a one-shot generator, not a
build step: run it, commit the HTML it writes, and the site stays vanilla
static. Edit the data below and re-run to regenerate all pages.

    python3 build_locations.py

Pricing shown in the services recap mirrors services.html, which stays the
source of truth. If prices change there, change SERVICES here too.
"""

import os
import re

SITE = "https://makeupandhairbyandreina.com"
HERE = os.path.dirname(os.path.abspath(__file__))
UP = "../../"  # locations/<slug>/index.html -> repo root

# Mirrors the bridal + quinceanera tables in services.html.
SERVICES = [
    ("Bridal Hair or Makeup", "$175 per service"),
    ("Bridal Party, per person", "$125 per service"),
    ("Trial Session", "$175 per service"),
    ("Quincea&ntilde;era Hair", "$175&ndash;$200"),
    ("Quincea&ntilde;era Makeup", "$175"),
    ("Flower Girls (7 &amp; under)", "from $25"),
]

CITIES = [
    {
        "slug": "dallas",
        "name": "Dallas",
        "county": "Dallas County",
        "kicker": "Dallas County &middot; The Whole Metro",
        "title": "Bridal Hair &amp; Makeup Artist, Dallas TX",
        "desc": "On-location bridal hair and makeup artist serving Dallas, TX from $175 per service. Andreina travels to the Adolphus, Arlington Hall and your own venue.",
        "intro": [
            "Andreina is an on-location bridal hair and makeup artist serving Dallas, TX. She does not keep a chair in a salon somewhere off Greenville Avenue and wait for you to find parking &mdash; she loads the kit and comes to whichever downtown hotel suite, Uptown high-rise, or east-side bungalow your party has taken over for the morning.",
            "Dallas weddings cover an enormous range, from a ballroom at a landmark hotel to a garden courtyard to a converted pump house on the lake. Those rooms do not light a face the same way, and a look built for one will not hold in another. Hair and makeup are both done in-house, so one artist carries the whole brief rather than two vendors negotiating a timeline over text.",
        ],
        "venues_intro": "Dallas has more wedding venues than any list can hold. These are ones Andreina knows well:",
        "venues": [
            ("The Adolphus Hotel", "The downtown landmark, with five ballrooms including the Governor&rsquo;s and the Grand. Deep interiors and warm hotel lighting, which take a richer look than a garden ceremony would."),
            ("Arlington Hall at Lee Park", "A classical mansion on Turtle Creek surrounded by manicured gardens. Formal and symmetrical, and it suits a cleaner, more timeless finish than anything heavily contoured."),
            ("Marie Gabrielle Restaurant &amp; Gardens", "Courtyard gardens with a gazebo and cascading water, built for outdoor ceremonies. Full daylight most of the day, so the makeup is finished to sit correctly in it rather than under a mirror."),
            ("The Filter Building on White Rock Lake", "A converted pump house on the lake taking around 200 guests, with a generous getting-ready suite. Industrial brick and hard light &mdash; a room that carries more contrast than most."),
        ],
        "travel": "A flat travel fee of $65 is assessed for Dallas.",
        "quince": "Dallas quincea&ntilde;eras are a large part of Andreina's calendar, and she works in both English and Spanish. The honouree, her damas, and the mothers are all priced per person.",
        "nearby": ["Rockwall", "Heath", "Forney", "Terrell"],
    },
    {
        "slug": "rockwall",
        "name": "Rockwall",
        "county": "Rockwall County",
        "kicker": "Rockwall County &middot; Home Studio",
        "title": "Bridal Hair &amp; Makeup in Rockwall, TX",
        "desc": "On-location bridal hair and makeup in Rockwall, TX from $175 per service. Andreina works from her Rockwall studio and travels to your venue. Book your date.",
        "intro": [
            "Andreina is a bridal hair and makeup artist in Rockwall, TX, and this is where she is based. Her studio is here, which means no highway math on your wedding morning and no artist arriving flustered twenty minutes behind schedule. She is set up and working before the day has a chance to get ahead of you.",
            "Being local changes what the morning feels like. There is time to do the trial properly, time to adjust, and time to get your party through the chairs without anyone being rushed. Hair and makeup are both done in-house, so you are coordinating with one artist instead of two calendars.",
        ],
        "venues_intro": "For a small county, Rockwall covers a lot of ground &mdash; a lakefront ballroom at one end, an actual castle at the other. Andreina regularly works at:",
        "venues": [
            ("The Castle at Rockwall", "Over 8,000 square feet of castle-inspired architecture seating up to 350. The scale of the room carries a bolder, more editorial look than a softer venue would."),
            ("The Parrish House", "A restored mansion downtown taking 160 guests, all warm woodwork and big windows. Forgiving light, which means a softer finish holds up without needing to be rebuilt for photographs."),
            ("Hilton Dallas/Rockwall Lakefront", "Right on the water, with a pergola outside for the ceremony and a ballroom indoors for afterwards. Take a suite upstairs and the party never has to leave the building."),
            ("Little Wren Weddings &amp; Events", "A short walk from the old downtown square, with space inside and out. Popular with couples keeping the guest list tight and the day close to home."),
        ],
        "travel": "Rockwall is home base, so travel sits at the lowest flat rate on the schedule &mdash; $45 for the first 30 miles.",
        "quince": "Rockwall quincea&ntilde;eras are a steady part of Andreina's calendar, and the court is welcome. Chambelanas and damas are priced per person at the same rate as a bridal party.",
        "nearby": ["Dallas", "Heath", "Royse City", "Forney"],
    },
    {
        "slug": "royse-city",
        "name": "Royse City",
        "county": "Rockwall County",
        "kicker": "Rockwall County &middot; Fifteen Minutes Out",
        "title": "Bridal Hair &amp; Makeup in Royse City, TX",
        "desc": "On-location bridal hair and makeup in Royse City, TX from $175 per service. Andreina travels to The Pearl at Sabine Creek, Castle Waterford and your venue.",
        "intro": [
            "Looking for a bridal hair and makeup artist in Royse City, TX? Andreina travels to you. Royse City sits about fifteen minutes up I-30 from her Rockwall studio, which makes it one of the easiest mornings on her calendar and one of the cheapest on travel.",
            "The venues out here do not all want the same face. A colonial mansion and an Irish castle call for different levels of contrast, and Andreina builds to the room rather than applying one house look to every bride who books her.",
        ],
        "venues_intro": "A handful of square miles holding a genuinely odd variety of venues. Andreina regularly works at:",
        "venues": [
            ("The Pearl at Sabine Creek", "A colonial-style mansion on eight wooded acres. Private, elegant, and suited to a timeless look that will not date in the album ten years from now."),
            ("Castle Waterford", "Eleven acres of genuine Irish-castle stonework. The interiors are dark and dramatic enough to carry a deeper, bolder look that would overpower a lighter room."),
            ("Country Charm Events", "An easy-going barn with outdoor space, built for weddings of about 120. Nothing fussy about it, which suits a lighter, more natural finish."),
        ],
        "travel": "The drive is about fifteen minutes up I-30 from the studio, which keeps Royse City in the lowest travel tier.",
        "quince": "Royse City and Fate families book Andreina for quincea&ntilde;eras as often as weddings. The honouree, her court, and mum can all be worked into one timeline.",
        "nearby": ["Rockwall", "Greenville", "Princeton", "Terrell"],
    },
    {
        "slug": "forney",
        "name": "Forney",
        "county": "Kaufman County",
        "kicker": "Kaufman County &middot; South of Rockwall",
        "title": "On-Location Bridal Hair &amp; Makeup, Forney TX",
        "desc": "On-location bridal hair and makeup in Forney, TX from $175 per service. Andreina travels to The Delanie Venue, The Ritz on Buffalo Creek and your venue.",
        "intro": [
            "Andreina is an on-location bridal hair and makeup artist serving Forney, TX, about twenty minutes south of her Rockwall studio. She brings the full kit to whichever suite you are getting ready in, so nobody in your party is driving to an appointment on the morning of the wedding.",
            "Forney's venues run bright and glass-heavy, and that matters more for makeup than most brides expect. Hard daylight flattens a look that was built for a dim salon mirror. Andreina finishes for the light you will actually be photographed in.",
        ],
        "venues_intro": "Two very different rooms, a few miles apart: one built almost entirely of glass, the other a family estate down on the creek. Andreina regularly works at:",
        "venues": [
            ("The Delanie Venue", "A greenhouse-styled reception hall seating 280 under full-height glass. There are two dressing suites, and one is fitted with real beauty stations &mdash; rarer than it ought to be, and it makes the morning noticeably easier."),
            ("The Ritz on Buffalo Creek", "A family-owned five-acre estate with waterfront ceremony space and an ornamental staircase running down from the bridal suite &mdash; worth building the timeline around for photographs."),
        ],
        "travel": "Forney is about twenty minutes south of Rockwall, comfortably inside the core service area on the flat travel schedule.",
        "quince": "Forney quincea&ntilde;eras get the same treatment as bridal work: a trial first, then a day-of timeline that gets the whole court through without anyone waiting an hour in a robe.",
        "nearby": ["Dallas", "Terrell", "Heath", "Rockwall"],
    },
    {
        "slug": "heath",
        "name": "Heath",
        "county": "Rockwall County",
        "kicker": "Rockwall County &middot; On Lake Ray Hubbard",
        "title": "On-Location Bridal Hair &amp; Makeup, Heath TX",
        "desc": "On-location bridal hair and makeup in Heath, TX from $175 per service. Minutes from Andreina's Rockwall studio, so travel stays at the lowest flat rate.",
        "intro": [
            "Andreina is a bridal hair and makeup artist working on-location in Heath, TX. Heath is a few minutes from her Rockwall studio, which puts it in the lowest travel tier and makes for one of the least rushed mornings she does.",
            "Light off the water is bright, directional, and unkind to a heavy hand. Whether it is eight people at a lake house or a party of twelve, the look is built to survive a Texas afternoon outdoors and still read properly once the reception lighting takes over.",
        ],
        "venues_intro": "The shoreline here holds some of the better-looking settings anywhere east of Dallas. Andreina regularly works at:",
        "venues": [
            ("Hidden Creek Events", "An all-inclusive venue in the woods off Chris Cuny Parkway, taking up to 300. A barn done in vintage style, a gazebo, and a walk down through the trees to the ceremony. The bridal suite is one of the few locally with vanity stations and lighting actually designed for getting ready in."),
        ],
        "travel": "Heath borders Rockwall, so you get full on-location service at the lowest flat travel rate on the schedule.",
        "quince": "Heath and McLendon-Chisholm families book Andreina for quincea&ntilde;eras through the spring and autumn. Trials are strongly recommended and are priced the same as the day-of service.",
        "nearby": ["Rockwall", "Dallas", "Forney", "Terrell"],
    },
    {
        "slug": "quinlan",
        "name": "Quinlan",
        "county": "Hunt County",
        "kicker": "Hunt County &middot; White Sparrow Country",
        "title": "Bridal Hair &amp; Makeup in Quinlan, TX",
        "desc": "Getting married at The White Sparrow Barn? On-location bridal hair and makeup in Quinlan, TX from $175. Andreina comes to your suite. Book your date today.",
        "intro": [
            "Searching for a bridal hair and makeup artist in Quinlan, TX? Andreina travels out to you. Quinlan pulls couples from well outside Texas on the strength of one barn, and the getting-ready logistics are usually the part nobody plans until late.",
            "She arrives wherever your party has landed &mdash; the bridal suite, a rental, a hotel in Greenville &mdash; so you are not splitting the morning between two locations. The barn's whitewashed interior throws a lot of bounced light, and the look is finished to sit correctly in it rather than disappear.",
        ],
        "venues_intro": "A small town carrying a reputation far bigger than its population. Andreina regularly works at:",
        "venues": [
            ("The White Sparrow Barn", "The reason people fly into Dallas for a Quinlan wedding. Family-run, set in an oak field, with whitewashed walls, ceilings that go up forever, and dressing suites on site for 200 guests."),
            ("Paradise Ranch of Texas", "Over 400 acres in the pines off County Road 2300, with an open-air venue, twinkle-lit trees, and cabins on site for a party that is staying the weekend."),
            ("The Meadows at Peninsula Ranch", "Up to 250 guests, with a reception hall, three cabins, an indoor pool and hot tub &mdash; set up for couples turning the wedding into a two-day event."),
        ],
        "travel": "Quinlan is roughly thirty-five minutes southeast of Rockwall. Travel is a flat fee by distance, so the full cost is clear before you book.",
        "quince": "Hunt County quincea&ntilde;eras are welcome, court included. If the venue is a barn, say so at enquiry &mdash; humidity and open-air receptions change what Andreina reaches for.",
        "nearby": ["Greenville", "Terrell", "Royse City", "Rockwall"],
    },
    {
        "slug": "terrell",
        "name": "Terrell",
        "county": "Kaufman County",
        "kicker": "Kaufman County &middot; Barn &amp; Estate Country",
        "title": "Bridal Hair &amp; Makeup in Terrell, TX",
        "desc": "On-location bridal hair and makeup for Terrell, TX barn weddings. HR Ranch, The Establishment, Chandelier Farms. From $175 per service. Check your date.",
        "intro": [
            "Andreina is an on-location bridal hair and makeup artist serving Terrell, TX, about twenty-five minutes south of the studio. Kaufman County books a lot of weddings now, mostly in barns and estates, and most of them have proper getting-ready space built in.",
            "Barn weddings are long days, frequently outdoors, often in heat. That is a different brief from a hotel ballroom. Makeup gets built to survive the afternoon rather than just to look right in the first hour, and hair is set to hold through the reception instead of collapsing by the first dance.",
        ],
        "venues_intro": "Terrell has quietly assembled one of the stronger barn-and-estate line-ups in the region. Andreina regularly works at:",
        "venues": [
            ("HR Ranch", "A newer addition to the county, built around a barn with water on the land. There is a separate bridal house rather than a back room, which makes a real difference to a party of eight."),
            ("The Establishment Barn", "Seven and a half thousand square feet out at Able Springs. New construction, but fitted with salvaged nineteenth-century leaded glass and doors made by hand, so it reads far older than it is."),
            ("Chandelier Farms", "A luxury East Texas estate drawing on European craftsmanship &mdash; the barn-luxe end of the county, and a setting that carries a more polished look."),
        ],
        "travel": "Terrell is a twenty-five minute run south from the studio, comfortably inside the core service area on the flat distance-based fee.",
        "quince": "Terrell and Kaufman quincea&ntilde;eras book early, particularly for autumn Saturdays. The honouree, her damas, and family are all priced per person.",
        "nearby": ["Forney", "Rockwall", "Quinlan", "Heath"],
    },
    {
        "slug": "greenville",
        "name": "Greenville",
        "county": "Hunt County",
        "kicker": "Hunt County &middot; The I-30 Corridor",
        "title": "Bridal Hair &amp; Makeup in Greenville, TX",
        "desc": "On-location bridal hair and makeup in Greenville, TX from $175 per service. Andreina travels to On The Rock, Under The Wildwood and Davis &amp; Grey Farms.",
        "intro": [
            "Andreina is a bridal hair and makeup artist travelling on-location to Greenville, TX, a straight run northeast up I-30 from her Rockwall studio. Hunt County is working-ranch country, and its wedding venues have the wide-open light to match.",
            "That light is the whole consideration here. Golden hour on an open field is glorious in photographs and merciless on anything applied too heavily. Andreina builds for it directly, and keeps the party coordinated so the timeline does not slip while the photographer is waiting.",
        ],
        "venues_intro": "Hunt County is thick with ranch and barn venues once you get past the town limits. Andreina regularly works at:",
        "venues": [
            ("On The Rock Wedding Barn", "A barn-chapel on Retazo Ranch, seven acres of working cattle land. There is a pond, a fire pit, and room for 200 whether the reception ends up inside or out."),
            ("Under The Wildwood", "Takes 250 across indoor and outdoor space, with a deep covered patio for when the weather turns, a catering kitchen, and separate suites for each party."),
            ("Davis &amp; Grey Farms", "A farm setting popular with Greenville-area couples for romantic outdoor ceremonies, with the reception kept on the property."),
        ],
        "travel": "Half an hour up I-30 from the studio, with travel charged as a flat fee by distance rather than by the hour.",
        "quince": "Greenville quincea&ntilde;eras are welcome, and the court can be worked into the same morning. Ask about timing early if the party runs past six people.",
        "nearby": ["Quinlan", "Royse City", "Sulphur Springs", "Princeton"],
    },
    {
        "slug": "sulphur-springs",
        "name": "Sulphur Springs",
        "county": "Hopkins County",
        "kicker": "Hopkins County &middot; East Texas",
        "title": "Bridal Hair &amp; Makeup Sulphur Springs TX",
        "desc": "On-location bridal hair and makeup in Sulphur Springs, TX from $175. The Black Oak, the Country Club and more, with a flat travel fee set by distance.",
        "intro": [
            "Andreina is an on-location bridal hair and makeup artist who travels out to Sulphur Springs, TX. Hopkins County is the furthest she goes on a regular basis &mdash; call it an hour on the interstate &mdash; and that distance is worth building the morning around properly.",
            "Booking an artist who travels means the whole party gets ready in one place, which matters more the further out you are &mdash; there is no local salon run that works when the venue is twenty minutes from town. Hair and makeup are both done in-house, so one arrival covers everything.",
        ],
        "venues_intro": "The range here runs from polished barns through to a proper country club. Andreina regularly works at:",
        "venues": [
            ("The Black Oak", "The area's best-known wedding venue, minutes off I-30, blending rustic warmth with more polished detailing than the barn category usually offers."),
            ("Sulphur Springs Country Club", "A contemporary ballroom carrying just enough rustic detail, wrapped by the golf course and lakes, with a deck outside once the dancing starts."),
            ("Hopkins County Regional Civic Center", "The biggest room in Hopkins County, and flexible enough indoors and out to absorb a guest list of almost any size."),
            ("The Oaks Bed &amp; Breakfast", "Aimed squarely at small weddings, with a walled garden for the ceremony and reception space running inside and out."),
        ],
        "travel": "This is the long one &mdash; roughly an hour east on I-30, which puts it in the upper travel tiers. The fee is quoted before you book, so nothing lands on the invoice unannounced.",
        "quince": "Hopkins County quincea&ntilde;eras are worth booking well ahead given the distance &mdash; Andreina holds one booking per day out here so the timeline never gets squeezed.",
        "nearby": ["Greenville", "Quinlan", "Royse City", "Rockwall"],
    },
    {
        "slug": "princeton",
        "name": "Princeton",
        "county": "Collin County",
        "kicker": "Collin County &middot; Near Lake Lavon",
        "title": "Bridal Hair &amp; Makeup in Princeton, TX",
        "desc": "On-location bridal hair and makeup in Princeton, TX from $175 per service. Andreina travels to The Cinnamon Barn, 1899 Farmhouse and your Collin County venue.",
        "intro": [
            "Andreina is a bridal hair and makeup artist working on-location in Princeton, TX, roughly forty minutes north of her Rockwall studio. This corner of Collin County has grown quickly, and the venues that came with it are mostly small farms and ranches scattered around Lavon.",
            "The venues here skew intimate, often under 150 guests, which changes the morning. Smaller party, more time per person, and a look that can carry more detail because it will be seen close up rather than from the back of a 300-seat room.",
        ],
        "venues_intro": "Small farm and ranch venues are scattered all around Lavon. Andreina regularly works at:",
        "venues": [
            ("The Cinnamon Barn", "A newly built barn on over nine acres minutes from Lake Lavon, taking up to 225 guests indoors with manicured lawns and outdoor space alongside."),
            ("1899 Farmhouse", "Eleven acres of outdoor wedding and event space minutes from Lavon Lake, at the relaxed and rustic end of the county."),
            ("The Penrose House", "A private, gated property on FM 3364 built specifically for celebrations of twenty to fifty guests, with exclusive use of the whole property."),
            ("Magnolia Creek Ranch", "Twelve acres of private land a quarter-hour out from McKinney, arranged indoors and out for weddings topping out around 130."),
        ],
        "travel": "Princeton is roughly forty minutes north of Rockwall. Andreina travels throughout Collin County at a flat fee set by distance.",
        "quince": "Collin County quincea&ntilde;eras are a growing part of the calendar. Trials are recommended, and the court is priced per person alongside the honouree.",
        "nearby": ["Royse City", "Greenville", "Rockwall", "Heath"],
    },
]

SLUGS = {c["name"]: c["slug"] for c in CITIES}

# --------------------------------------------------------------------------
# Template
# --------------------------------------------------------------------------

NAV = """<nav style="position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(255,250,248,0.97);backdrop-filter:blur(8px);border-bottom:1px solid rgba(59,26,58,0.08);">
  <div class="section-wrap" style="height:72px;display:flex;align-items:center;justify-content:space-between;">
    <a href="{up}index.html" style="text-decoration:none;">
      <span class="display" style="font-size:17px;color:var(--brand);letter-spacing:0.08em;">Makeup &amp; Hair</span>
      <span class="display-italic" style="font-size:13px;color:var(--gold);margin-left:6px;">by Andreina</span>
    </a>
    <div class="desktop-nav" style="display:flex;align-items:center;gap:36px;">
      <a href="{up}services.html" class="nav-link">Services</a>
      <a href="{up}gallery.html"  class="nav-link">Gallery</a>
      <a href="{up}about.html"    class="nav-link">About</a>
      <a href="{up}blog.html"     class="nav-link">Blog</a>
      <a href="{up}contact.html"  class="nav-link">Contact</a>
    </div>
    <div class="desktop-nav" style="display:flex;align-items:center;gap:18px;">
      <a href="{up}contact.html" class="btn btn-dark" style="font-size:10px;padding:10px 22px;">Book Now</a>
    </div>
    <div class="mobile-trigger" style="display:none;align-items:center;gap:14px;">
      <button onclick="toggleMenu()" style="background:var(--brand);border:none;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,0.18);" aria-label="Menu">
        <svg width="20" height="20" fill="none" stroke="#fff" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>
      </button>
    </div>
  </div>
  <div id="mobile-menu" style="display:none;background:var(--white);border-top:1px solid rgba(59,26,58,0.07);padding:20px 28px 28px;">
    <div style="display:flex;flex-direction:column;gap:18px;">
      <a href="{up}services.html" onclick="closeMenu()" class="nav-link" style="padding:3px 0;border-bottom:1px solid rgba(59,26,58,0.07);">Services</a>
      <a href="{up}gallery.html"  onclick="closeMenu()" class="nav-link" style="padding:3px 0;border-bottom:1px solid rgba(59,26,58,0.07);">Gallery</a>
      <a href="{up}about.html"    onclick="closeMenu()" class="nav-link" style="padding:3px 0;border-bottom:1px solid rgba(59,26,58,0.07);">About</a>
      <a href="{up}blog.html"     onclick="closeMenu()" class="nav-link" style="padding:3px 0;border-bottom:1px solid rgba(59,26,58,0.07);">Blog</a>
      <a href="{up}contact.html"  onclick="closeMenu()" class="nav-link" style="padding:3px 0;">Contact</a>
      <a href="{up}contact.html" class="btn btn-dark" style="text-align:center;margin-top:6px;">Book Now</a>
    </div>
  </div>
</nav>"""

FOOTER = """<footer style="background:var(--brand);padding:64px 0 40px;">
  <div class="section-wrap">
    <div class="footer-grid" style="display:grid;grid-template-columns:1fr;gap:44px;margin-bottom:56px;">
      <div>
        <p class="display" style="font-size:16px;color:#fff;letter-spacing:0.06em;margin:0 0 6px;">MAKEUP &amp; HAIR</p>
        <p class="display-italic" style="font-size:14px;color:var(--gold);margin:0 0 20px;">by Andreina</p>
        <p style="font-size:13px;color:rgba(255,255,255,0.65);line-height:1.75;max-width:200px;margin:0 0 22px;">On-location bridal hair &amp; makeup serving the DFW area.</p>
      </div>
      <div>
        <p style="font-family:'Jost',sans-serif;font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:0.18em;color:rgba(255,255,255,0.55);margin:0 0 20px;">Navigation</p>
        <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px;">
          <li><a href="{up}index.html"    style="font-size:13px;color:rgba(255,255,255,0.7);text-decoration:none;">Home</a></li>
          <li><a href="{up}services.html" style="font-size:13px;color:rgba(255,255,255,0.7);text-decoration:none;">Services</a></li>
          <li><a href="{up}gallery.html"  style="font-size:13px;color:rgba(255,255,255,0.7);text-decoration:none;">Gallery</a></li>
          <li><a href="{up}about.html"    style="font-size:13px;color:rgba(255,255,255,0.7);text-decoration:none;">About</a></li>
          <li><a href="{up}blog.html"     style="font-size:13px;color:rgba(255,255,255,0.7);text-decoration:none;">Blog</a></li>
          <li><a href="{up}contact.html"  style="font-size:13px;color:rgba(255,255,255,0.7);text-decoration:none;">Contact</a></li>
        </ul>
      </div>
      <div>
        <p style="font-family:'Jost',sans-serif;font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:0.18em;color:rgba(255,255,255,0.55);margin:0 0 20px;">Areas Served</p>
        <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px;">
{arealinks}
        </ul>
      </div>
      <div>
        <p style="font-family:'Jost',sans-serif;font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:0.18em;color:rgba(255,255,255,0.55);margin:0 0 20px;">Contact</p>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <a href="tel:+19566406220" style="font-size:13px;color:rgba(255,255,255,0.7);text-decoration:none;">(956) 640-6220</a>
          <a href="mailto:wilsonandreina@yahoo.com" style="font-size:13px;color:rgba(255,255,255,0.7);text-decoration:none;">wilsonandreina@yahoo.com</a>
          <p style="font-size:13px;color:rgba(255,255,255,0.7);margin:0;">Rockwall, TX &middot; DFW</p>
        </div>
      </div>
    </div>
    <style>@media (min-width:768px){{ .footer-grid {{ grid-template-columns:2fr 1fr 1fr 1fr !important; }} }}</style>
    <div style="border-top:1px solid rgba(242,221,216,0.08);padding-top:28px;text-align:center;">
      <p style="font-size:11px;color:rgba(255,255,255,0.4);margin:0;letter-spacing:0.5px;">&copy; 2026 Makeup &amp; Hair by Andreina LLC. All rights reserved. &nbsp;&middot;&nbsp; <a href="{up}privacy.html" style="color:inherit;text-decoration:underline;">Privacy Policy</a></p>
    </div>
  </div>
</footer>"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Andreina LLC</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{site}/locations/{slug}/">
  <meta property="og:type"        content="website">
  <meta property="og:url"         content="{site}/locations/{slug}/">
  <meta property="og:title"       content="{title} | Andreina LLC">
  <meta property="og:description" content="{desc}">
  <meta property="og:image"       content="{site}/photos/branding/hero.jpeg">
  <meta name="twitter:card"        content="summary_large_image">
  <meta name="twitter:title"       content="{title} | Andreina LLC">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image"       content="{site}/photos/branding/hero.jpeg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:ital,wght@0,300;0,400;0,500;0,700;1,300&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{up}styles.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "serviceType": "On-location bridal hair and makeup",
    "name": "Bridal Hair & Makeup in {name}, TX",
    "url": "{site}/locations/{slug}/",
    "provider": {{
      "@type": "BeautySalon",
      "name": "Makeup & Hair by Andreina LLC",
      "url": "{site}",
      "image": "{site}/photos/branding/hero.jpeg",
      "telephone": "+1-956-640-6220",
      "email": "wilsonandreina@yahoo.com",
      "address": {{ "@type": "PostalAddress", "addressLocality": "Rockwall", "addressRegion": "TX", "addressCountry": "US" }},
      "sameAs": [
        "https://www.instagram.com/makeupandhairbyandreinallc",
        "https://www.tiktok.com/@makeupandhairbyandreina"
      ]
    }},
    "areaServed": {{
      "@type": "City",
      "name": "{name}",
      "containedInPlace": {{ "@type": "State", "name": "Texas" }}
    }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{site}/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Areas Served", "item": "{site}/locations/" }},
      {{ "@type": "ListItem", "position": 3, "name": "{name}, TX", "item": "{site}/locations/{slug}/" }}
    ]
  }}
  </script>
</head>
<body>

{nav}

<!-- ═══ PAGE HERO ═══ -->
<section style="padding:140px 0 72px;background:var(--blush);">
  <div class="section-wrap">
    <p class="sup" style="color:var(--gold);margin-bottom:14px;">{kicker}</p>
    <div class="gold-rule"></div>
    <h1 class="display" style="font-size:clamp(30px,5vw,60px);margin-bottom:20px;">
      <span style="display:block;color:var(--ink);">BRIDAL HAIR &amp; MAKEUP</span>
      <span style="display:block;color:var(--brand);">IN {upper}, TX</span>
    </h1>
    <p style="font-size:14px;line-height:1.9;color:#5a4455;max-width:560px;margin:0;">On-location hair and makeup for weddings, quincea&ntilde;eras, and special events in {name} and across {county}.</p>
  </div>
</section>

<!-- ═══ INTRO ═══ -->
<section class="section-pad" style="background:var(--white);">
  <div class="section-wrap">
    <div style="max-width:720px;">
{intro}
      <div class="fade-up" style="display:flex;flex-wrap:wrap;gap:14px;margin-top:34px;">
        <a href="{up}contact.html" class="btn btn-dark">Check Your Date</a>
        <a href="{up}gallery.html" class="btn btn-outline-dark">View Gallery</a>
      </div>
    </div>
  </div>
</section>

<!-- ═══ VENUES ═══ -->
<section class="section-pad" style="background:var(--blush);">
  <div class="section-wrap">
    <p class="sup fade-up" style="color:var(--gold);margin-bottom:14px;">Where She Works</p>
    <div class="gold-rule fade-up"></div>
    <h2 class="display fade-up" style="font-size:clamp(26px,4vw,46px);color:var(--ink);margin-bottom:8px;">{upper}</h2>
    <h2 class="display fade-up" style="font-size:clamp(26px,4vw,46px);color:var(--brand);margin-bottom:24px;">WEDDING VENUES</h2>
    <p class="fade-up" style="font-size:14px;line-height:1.95;color:#4a3542;max-width:680px;margin-bottom:40px;">{venues_intro}</p>
    <div style="display:flex;flex-direction:column;gap:16px;max-width:820px;">
{venues}
    </div>
    <p class="fade-up" style="font-size:12.5px;color:var(--muted);font-style:italic;line-height:1.8;margin:28px 0 0;max-width:680px;">{travel} <a href="{up}services.html#travel" style="color:var(--brand);text-decoration:underline;text-underline-offset:2px;">See the full travel schedule</a>.</p>
  </div>
</section>

<!-- ═══ SERVICES RECAP ═══ -->
<section class="section-pad" style="background:var(--white);">
  <div class="section-wrap">
    <p class="sup fade-up" style="color:var(--gold);margin-bottom:14px;">What She Offers</p>
    <div class="gold-rule fade-up"></div>
    <h2 class="display fade-up" style="font-size:clamp(26px,4vw,46px);color:var(--ink);margin-bottom:8px;">SERVICES IN</h2>
    <h2 class="display fade-up" style="font-size:clamp(26px,4vw,46px);color:var(--brand);margin-bottom:36px;">{upper}, TX</h2>
    <div class="fade-up" style="display:grid;grid-template-columns:1fr;gap:10px;max-width:640px;">
{services}
    </div>
    <p class="fade-up" style="font-size:12.5px;color:var(--muted);font-style:italic;margin:22px 0 28px;">Prices are per person, per service &mdash; hair and makeup are billed separately. Photoshoots and special events are quoted individually.</p>
    <div class="fade-up"><a href="{up}services.html" class="btn btn-outline-dark">See All Services &amp; Pricing</a></div>
  </div>
</section>

<!-- ═══ QUINCEAÑERA ═══ -->
<section class="section-pad" style="background:var(--ink);">
  <div class="section-wrap">
    <div class="split-wrap">
      <div class="split-img" style="width:100%;max-width:440px;flex-shrink:0;">
        <img src="{up}photos/quinceaera/quince-portrait.jpeg" alt="Quinceañera hair and makeup in {name}, TX" style="width:100%;aspect-ratio:4/5;object-fit:cover;object-position:center top;" loading="lazy">
      </div>
      <div style="flex:1;">
        <p class="sup fade-up" style="color:rgba(200,160,106,0.7);margin-bottom:14px;">Not Just Weddings</p>
        <div style="width:32px;height:1px;background:var(--gold);opacity:0.5;margin-bottom:22px;" class="fade-up"></div>
        <h2 class="display fade-up" style="font-size:clamp(24px,4vw,42px);color:#fff;margin-bottom:8px;">QUINCEA&Ntilde;ERAS IN</h2>
        <h2 class="display fade-up" style="font-size:clamp(24px,4vw,42px);color:var(--gold);margin-bottom:24px;">{upper}</h2>
        <p class="fade-up" style="font-size:14px;line-height:1.95;color:rgba(255,255,255,0.65);margin-bottom:18px;">{quince}</p>
        <p class="fade-up" style="font-size:14px;line-height:1.95;color:rgba(255,255,255,0.65);margin-bottom:30px;">Quincea&ntilde;era work is a real specialism of Andreina's, not a sideline &mdash; softer than bridal where it should be, and built to survive a full night of dancing and photographs.</p>
        <div class="fade-up"><a href="{up}contact.html" class="btn btn-outline-white">Book Andreina</a></div>
      </div>
    </div>
  </div>
</section>

<!-- ═══ GALLERY STRIP ═══ -->
<section class="section-pad-sm" style="background:var(--white);">
  <div class="section-wrap">
    <div class="gallery-grid fade-up">
      <div class="gallery-item"><img src="{up}photos/wedding/wedding-bride-doorway.jpeg" alt="Bridal hair and makeup {name} TX" loading="lazy"></div>
      <div class="gallery-item"><img src="{up}photos/wedding/wedding-braid-detail.jpeg" alt="Bridal hair detail {name} TX" loading="lazy"></div>
      <div class="gallery-item"><img src="{up}photos/wedding/wedding-bride-pergola.jpeg" alt="On-location bridal makeup {name} TX" loading="lazy"></div>
    </div>
    <p class="fade-up" style="text-align:center;margin:26px 0 0;"><a href="{up}gallery.html" class="btn btn-outline-dark">View Full Portfolio</a></p>
  </div>
</section>

<!-- ═══ NEARBY ═══ -->
<section class="section-pad-sm" style="background:var(--blush);">
  <div class="section-wrap" style="text-align:center;">
    <h2 class="display fade-up" style="font-size:clamp(20px,3vw,30px);color:var(--brand);margin-bottom:8px;">ALSO SERVING NEAR {upper}</h2>
    <div class="gold-rule fade-up" style="margin:0 auto 22px;"></div>
    <p class="fade-up" style="font-size:13.5px;line-height:1.95;color:#4a3542;max-width:640px;margin:0 auto;">Andreina works out of Rockwall, TX and travels across the DFW metro and East Texas &mdash; including {nearby}, and beyond. <a href="{up}contact.html" style="color:var(--brand);text-decoration:underline;text-underline-offset:2px;">Ask about your venue</a>.</p>
  </div>
</section>

<!-- ═══ CTA ═══ -->
<section class="section-pad-sm" style="background:var(--white);">
  <div class="section-wrap" style="text-align:center;">
    <h2 class="display-italic fade-up" style="font-size:clamp(26px,4vw,40px);color:var(--brand);margin:0 0 10px;">Ready to book {name}?</h2>
    <p class="fade-up" style="font-size:13.5px;color:#5a4455;line-height:1.9;max-width:460px;margin:0 auto 28px;">Send over your date and venue and Andreina will come back with availability and a quote for your party.</p>
    <div class="fade-up"><a href="{up}contact.html" class="btn btn-dark">Get in Touch</a></div>
  </div>
</section>

{footer}

<script src="{up}main.js"></script>
</body>
</html>
"""


def venue_html(name, blurb):
    return (
        '      <div class="fade-up" style="background:var(--white);border-left:2px solid var(--gold);padding:22px 26px;">\n'
        '        <h3 style="font-family:\'Cormorant Garamond\',serif;font-weight:400;font-size:21px;'
        'color:var(--brand);margin:0 0 8px;">%s</h3>\n'
        '        <p style="font-size:13.5px;line-height:1.8;color:#5a4455;margin:0;">%s</p>\n'
        '      </div>' % (name, blurb)
    )


def service_html(label, price):
    return (
        '      <div style="display:flex;justify-content:space-between;align-items:center;gap:20px;'
        'background:rgba(242,221,216,0.4);border:1px solid rgba(59,26,58,0.08);padding:16px 22px;">\n'
        '        <span style="font-size:13.5px;color:#4a3542;">%s</span>\n'
        '        <span style="font-family:\'Cormorant Garamond\',serif;font-size:16px;color:var(--brand);'
        'white-space:nowrap;">%s</span>\n'
        '      </div>' % (label, price)
    )


def nearby_html(towns, up):
    out = []
    for t in towns:
        slug = SLUGS.get(t)
        if slug:
            out.append('<a href="%slocations/%s/" style="color:var(--brand);text-decoration:underline;'
                       'text-underline-offset:2px;">%s</a>' % (up, slug, t))
        else:
            out.append(t)
    return ", ".join(out)


def area_links(up, current):
    rows = []
    for c in CITIES:
        if c["slug"] == current:
            rows.append('          <li><span style="font-size:13px;color:var(--gold);">%s, TX</span></li>' % c["name"])
        else:
            rows.append('          <li><a href="%slocations/%s/" style="font-size:13px;color:rgba(255,255,255,0.7);'
                        'text-decoration:none;">%s, TX</a></li>' % (up, c["slug"], c["name"]))
    return "\n".join(rows)


def build(city):
    intro = "\n".join(
        '      <p class="fade-up" style="font-size:15px;line-height:2;color:#4a3542;margin:0 0 20px;">%s</p>' % p
        for p in city["intro"]
    )
    return PAGE.format(
        site=SITE,
        up=UP,
        slug=city["slug"],
        name=city["name"],
        upper=city["name"].upper(),
        county=city["county"],
        kicker=city["kicker"],
        title=city["title"],
        desc=city["desc"],
        intro=intro,
        venues_intro=city["venues_intro"],
        venues="\n".join(venue_html(n, b) for n, b in city["venues"]),
        travel=city["travel"],
        quince=city["quince"],
        services="\n".join(service_html(l, p) for l, p in SERVICES),
        nearby=nearby_html(city["nearby"], UP),
        nav=NAV.format(up=UP),
        footer=FOOTER.format(up=UP, arealinks=area_links(UP, city["slug"])),
    )


def strip_entities(s):
    """Approximate rendered length for SEO length checks."""
    return re.sub(r"&[a-zA-Z]+;", "x", s)



HUB_UP = "../"

HUB = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Areas Served | Makeup &amp; Hair by Andreina</title>
  <meta name="description" content="On-location bridal hair and makeup across Rockwall, Kaufman, Hunt, Hopkins and Collin counties. Find Andreina's service area and city pages here.">
  <link rel="canonical" href="{site}/locations/">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{site}/locations/">
  <meta property="og:title" content="Areas Served | Makeup &amp; Hair by Andreina">
  <meta property="og:description" content="On-location bridal hair and makeup across Rockwall, Kaufman, Hunt, Hopkins and Collin counties.">
  <meta property="og:image" content="{site}/photos/branding/hero.jpeg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:ital,wght@0,300;0,400;0,500;0,700;1,300&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{up}styles.css">
</head>
<body>

{nav}

<section style="padding:140px 0 72px;background:var(--blush);">
  <div class="section-wrap">
    <p class="sup" style="color:var(--gold);margin-bottom:14px;">Where She Travels</p>
    <div class="gold-rule"></div>
    <h1 class="display" style="font-size:clamp(32px,5vw,60px);margin-bottom:20px;">
      <span style="display:block;color:var(--ink);">AREAS</span>
      <span style="display:block;color:var(--brand);">SERVED</span>
    </h1>
    <p style="font-size:14px;line-height:1.9;color:#5a4455;max-width:560px;margin:0;">Andreina works from a home studio in Rockwall, TX and travels on-location across the DFW metro and East Texas. Travel is a flat fee set by distance.</p>
  </div>
</section>

<section class="section-pad" style="background:var(--white);">
  <div class="section-wrap">
    <div style="display:grid;grid-template-columns:1fr;gap:14px;max-width:900px;" class="city-grid">
{cards}
    </div>
    <style>@media (min-width:640px){{ .city-grid {{ grid-template-columns:repeat(2,1fr) !important; }} }}
           @media (min-width:1000px){{ .city-grid {{ grid-template-columns:repeat(3,1fr) !important; }} }}</style>
    <p class="fade-up" style="font-size:13.5px;color:#5a4455;line-height:1.9;margin:40px 0 0;max-width:620px;">Not on the list? Andreina regularly travels beyond these cities. <a href="{up}contact.html" style="color:var(--brand);text-decoration:underline;text-underline-offset:2px;">Send over your venue</a> and she will confirm availability and travel.</p>
  </div>
</section>

{footer}

<script src="{up}main.js"></script>
</body>
</html>
"""


def hub_card(city, up):
    return (
        '      <a href="%slocations/%s/" class="service-card fade-up" style="text-decoration:none;display:block;">\n'
        '        <h3>%s, TX</h3>\n'
        '        <p>%s</p>\n'
        '      </a>' % (up, city["slug"], city["name"], city["county"])
    )


def build_hub():
    return HUB.format(
        site=SITE,
        up=HUB_UP,
        nav=NAV.format(up=HUB_UP),
        footer=FOOTER.format(up=HUB_UP, arealinks=area_links(HUB_UP, None)),
        cards="\n".join(hub_card(c, HUB_UP) for c in CITIES),
    )


def main():
    for city in CITIES:
        d = os.path.join(HERE, "locations", city["slug"])
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "index.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build(city))

        full_title = strip_entities(city["title"] + " | Andreina LLC")
        desc = strip_entities(city["desc"])
        flags = []
        if not 50 <= len(full_title) <= 60:
            flags.append("title %d" % len(full_title))
        if not 150 <= len(desc) <= 160:
            flags.append("desc %d" % len(desc))
        print("%-16s %s" % (city["slug"], ("FLAG: " + ", ".join(flags)) if flags else "ok"))

    with open(os.path.join(HERE, "locations", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(build_hub())
    print("%-16s ok" % "locations/index")


if __name__ == "__main__":
    main()
