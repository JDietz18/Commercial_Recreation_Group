"""Page bodies for the CRG site. Facts come from crgplay.com (October 2026).
Elements with data-draft still need CRG to confirm them (add ?draft to any URL)."""

SERVE = ('Are you part of a school, church, apartment complex, daycare, park, HOA or any '
         'other entity that is need of commercial recreational products? We are one of the '
         'largest commercial dealers for playground equipment in the state of Indiana.')

PRODUCTS = [
    dict(id='play-systems', icon='users', name='Play systems', photo='main.jpg',
         alt='Playground with a green spiral slide, climbing wall and rope net',
         short='Playcraft Systems structures, made in the USA and installed by our crews.',
         body='CRG is the Indiana representative for Playcraft Systems. Playcraft structures, including the R5, R3.5 and Revolution lines, are powder-coated for durability, made in the USA and backed by Playcraft’s warranty programs. We help you choose equipment that fits your facility, your users and your budget, then install it.',
         points=['Playcraft Systems structures', 'R5, R3.5 and Revolution lines', 'Made in the USA, powder-coated', 'Inclusive and accessible play areas']),
    dict(id='shades-shelters', icon='umbrella', name='Shades &amp; shelters', photo='getting-close-sketch.jpg',
         alt='Tensioned shade canopies over a splash plaza at dusk',
         short='Shade structures and park shelters that protect from sun and rain.',
         body='Shade structures and park shelters keep guests comfortable and protect them from harmful UV rays and rain. We add shade to playgrounds, seating areas and preschool play yards for schools, churches, daycares and apartment communities.',
         points=['Playground shade structures', 'Park shelters and pavilions', 'Shade for preschool and daycare play yards']),
    dict(id='free-standing', icon='rotate-cw', name='Free-standing play', photo=None,
         short='Swings, spinners, climbers and stand-alone play events.',
         body='Swings, spinners, climbers and other stand-alone play events, on their own or added to an existing playground.',
         points=['Swings for all ages', 'Spinners and climbers', 'Add-ons for existing playgrounds']),
    dict(id='safety-surfacing', icon='layers', name='Safety surfacing', photo=None,
         short='Poured-in-place rubber, artificial grass, tiles and mulch.',
         body='The right surface under play equipment, matched to your site, budget and upkeep.',
         points=['Poured-in-place rubber', 'Artificial grass', 'Rubber tiles', 'Rubber mulch and wood playground mulch', 'Borders and access ramps']),
    dict(id='site-amenities', icon='armchair', name='Site amenities', photo=None,
         short='Benches, picnic tables, bike racks and receptacles.',
         body='Outdoor furniture built from durable materials for parks, schools and public spaces, with custom options.',
         points=['Benches in many styles', 'Picnic tables, including wheelchair-accessible', 'Bike racks', 'Trash and recycling receptacles']),
    dict(id='sports', icon='trophy', name='Sports equipment', photo=None,
         short='Equipment for courts, fields and sports complexes.',
         body='Athletic equipment for schools, parks and communities, plus help designing sports complexes.',
         points=['Basketball goals and courts', 'Soccer and football goals', 'Baseball and volleyball equipment']),
    dict(id='dog-parks', icon='dog', name='Dog parks', photo=None,
         short='Agility equipment, fencing and amenities for dog parks.',
         body='Everything for a safe dog park at an apartment community or public park.',
         points=['Agility equipment', 'Commercial-grade fencing and surfacing', 'Shade, water fountains and waste stations']),
    dict(id='design-install', icon='hard-hat', name='Planning, design &amp; installation', photo='hayswood-render.jpg',
         alt='Rendered site plan of the Possibility Playground at Hayswood Nature Reserve',
         short='Design and installation of every product we offer.',
         body='We offer planning, design and installation of every product we sell. Our account reps are Certified Playground Safety Inspectors, and our installation crews make sure your equipment is installed correctly and up to current safety standards.',
         points=['Site planning and playground design', 'Certified Playground Safety Inspectors', 'Installation by our own crews', 'Financing through Navitas Credit Corp.']),
]

PROJECTS = [
    dict(photo='hayswood-render.jpg', title='Possibility Playground', tags='Hayswood Nature Reserve · Corydon, IN',
         cat='playground', real=True,
         alt='Rendered site plan of the Possibility Playground at Hayswood Nature Reserve'),
    dict(photo='main.jpg', title='Community park playground', tags='Playground', cat='playground',
         alt='Playground with a green spiral slide, climbing wall and rope net'),
    dict(photo='asla-sunset.jpg', title='Modern play structure', tags='Playground', cat='playground',
         alt='Modern play structure with a round canopy at sunset'),
    dict(photo='color-book-cover.jpg', title='Farm-themed play barn', tags='Themed', cat='themed',
         alt='Red barn-themed play structure in a field of sunflowers'),
    dict(photo='crisp-wet-morning.jpg', title='Timber tower playground', tags='Themed', cat='themed',
         alt='Large timber-look play structure with towers and tube slides'),
    dict(photo='getting-close-sketch.jpg', title='Shade canopy plaza', tags='Shade', cat='shade',
         alt='Tensioned shade canopies over a splash plaza at dusk'),
]

TESTIMONIALS = [
    ('This team is honest. They help beyond expectations. It is a blessing to work with such a good local company with Travis and Shane helping the community build recreation. They are a true pleasure to work with.',
     'Chris Stice', 'Deputy Director, Hamilton County Parks &amp; Recreation'),
    ('The proposal submitted by Hamilton County’s own, Commercial Recreation Group, was outstanding! The highly-regarded Noblesville firm went head-to-head with some of the nation’s largest playground companies and outclassed them with their proposal.',
     'Allen Patterson', 'Director, Hamilton County Parks &amp; Recreation'),
    ('From the design phase to the installation, he was there helping us through every inch of the way. Even though we had a very tight schedule, he was also able to meet our completion date. We love ours!',
     'Randy Morris', 'City of Kokomo'),
]

STEPS = [
    ('clipboard-list', 'Consult', 'Tell us about your site, who will use it, and your budget and timing.'),
    ('pencil-ruler', 'Design', 'We design a play area that fits your space and budget, and help you choose equipment.'),
    ('truck', 'Install', 'Our own crews install your equipment correctly and up to current safety standards.'),
    ('wrench', 'Support', 'Playcraft’s warranty programs, and a local team in Noblesville when you need us.'),
]


def build(h):
    icon, banner, cta, AUD = h['icon'], h['banner'], h['cta'], h['AUDIENCES']

    def section_head(eyebrow, title, lede='', id_='', draft=False, center=False):
        lede_html = f'<p class="crg-body-lg crg-section-head__lede"{" data-draft" if draft else ""}>{lede}</p>' if lede else ''
        return f'''<div class="crg-section-head{" crg-section-head--center" if center else ""}">
                <div>
                    <p class="crg-eyebrow">{eyebrow}</p>
                    <h2{f' id="{id_}"' if id_ else ""} class="crg-h1">{title}</h2>
                </div>
                {lede_html}
            </div>'''

    def project_card(p, cls='col-lg-4 col-md-6 col-sm-12'):
        return f'''<li class="card-container {cls} m-b30 {p['cat']}">
                    <a class="crg-project mfp-link" href="images/photos/{p['photo']}" title="{p['title']}">
                        <span class="crg-project__media"><img src="images/photos/{p['photo']}" alt="{p['alt']}" loading="lazy" width="1600" height="900"></span>
                        <span class="crg-project__body">
                            <span class="crg-project__title"{"" if p.get("real") else " data-draft"}>{p['title']}</span>
                            <span class="crg-project__tag">{p['tags']}</span>
                        </span>
                    </a>
                </li>'''

    audience_dups = '\n'.join(
        f'            <li class="crg-dup" aria-hidden="true">{icon(i)}<span>{label}</span></li>' for i, label in AUD)
    audience_strip = '\n'.join(
        f'            <li>{icon(i)}<span>{label}</span></li>' for i, label in AUD)

    # ------------------------------------------------------------------ Home
    offer_cards = '\n'.join(f'''                <div class="col-lg-3 col-md-6">
                    <a class="crg-card" href="products.html#{p['id']}">
                        <span class="crg-card__icon">{icon(p['icon'], 'crg-icon--xl')}</span>
                        <h3 class="crg-h3">{p['name']}</h3>
                        <p>{p['short']}</p>
                        <span class="crg-card__more">Learn more {icon('arrow-right', 'crg-icon--sm')}</span>
                    </a>
                </div>''' for p in PRODUCTS)

    steps = '\n'.join(f'''                <li class="col-lg-3 col-md-6">
                    <div class="crg-step">
                        <span class="crg-step__num">0{n}</span>
                        {icon(i, 'crg-icon--xl')}
                        <h3 class="crg-h3">{t}</h3>
                        <p>{d}</p>
                    </div>
                </li>''' for n, (i, t, d) in enumerate(STEPS, 1))

    featured = '\n'.join(project_card(p) for p in PROJECTS[:3])
    quotes = '\n'.join(f'''            <div class="col-lg-4">
                <figure class="crg-quote">
                    {icon('quote', 'crg-icon--xl')}
                    <blockquote><p>{q}</p></blockquote>
                    <figcaption><b>{who}</b><span>{role}</span></figcaption>
                </figure>
            </div>''' for q, who, role in TESTIMONIALS)

    home = f'''<section class="crg-hero" aria-labelledby="hero-title">
    <div class="crg-hero__copy">
        <p class="crg-eyebrow">Indiana playground dealer</p>
        <h1 id="hero-title" class="crg-display" data-split>Play spaces for every community</h1>
        <p class="crg-body-lg crg-hero__lede">We are one of the largest commercial dealers for playground equipment in the state of Indiana, with 25 years of experience installing commercial play spaces.</p>
        <div class="crg-actions">
            <a href="contact.html" class="crg-btn crg-btn--primary">Start a project {icon('arrow-right', 'crg-icon--md')}</a>
            <a href="projects.html" class="crg-btn crg-btn--outline">View projects</a>
        </div>
    </div>
    <div class="crg-hero__photo" data-slideshow aria-roledescription="carousel" aria-label="Project photos">
        <img class="crg-slide is-active" src="images/photos/asla-sunset.jpg" alt="Modern play structure with a round canopy at sunset" width="1600" height="900" fetchpriority="high">
        <img class="crg-slide" data-defer src="images/photos/main.jpg" alt="Playground with a green spiral slide, climbing wall and rope net" width="1600" height="900" loading="lazy" aria-hidden="true">
        <img class="crg-slide" data-defer src="images/photos/color-book-cover.jpg" alt="Red barn-themed play structure in a field of sunflowers" width="1600" height="900" loading="lazy" aria-hidden="true">
        <img class="crg-slide" data-defer src="images/photos/crisp-wet-morning.jpg" alt="Large timber-look play structure with towers and tube slides" width="1600" height="900" loading="lazy" aria-hidden="true">
        <div class="crg-hero__controls">
            <button type="button" class="crg-hero__dot" data-slide-to="0" aria-label="Show photo 1 of 4" aria-current="true"></button><button type="button" class="crg-hero__dot" data-slide-to="1" aria-label="Show photo 2 of 4" aria-current="false"></button><button type="button" class="crg-hero__dot" data-slide-to="2" aria-label="Show photo 3 of 4" aria-current="false"></button><button type="button" class="crg-hero__dot" data-slide-to="3" aria-label="Show photo 4 of 4" aria-current="false"></button>
            <button type="button" class="crg-hero__pause" data-motion-pause aria-pressed="false" aria-label="Pause animations">{icon('pause', 'crg-icon--md i-pause')}{icon('play', 'crg-icon--md i-play')}</button>
        </div>
    </div>
</section>
<div class="crg-audience-wrap">
<ul class="crg-audience" aria-label="Who we serve">
{audience_strip}
{audience_dups}
</ul>
</div>

<section class="section-full crg-serve" aria-labelledby="serve-title">
    <div class="container">
        <p class="crg-eyebrow">Who we serve</p>
        <h2 id="serve-title" class="crg-h1 crg-serve__statement" data-scrub-words>{SERVE}</h2>
        <a href="about.html" class="crg-btn crg-btn--light">About CRG {icon('arrow-right', 'crg-icon--md')}</a>
    </div>
</section>

<section class="section-full content-inner crg-section" aria-labelledby="offer-title">
    <div class="container">
        {section_head('What we offer', 'Everything for the play space', 'Playgrounds, shade, surfacing, sports equipment, site amenities and dog parks, with planning, design and installation of everything we sell.', 'offer-title')}
        <div class="row">
{offer_cards}
        </div>
    </div>
</section>

<section class="section-full content-inner crg-section crg-section--deep" aria-labelledby="featured-title">
    <div class="container">
        {section_head('Featured projects', 'Recent work', 'A look at play spaces we have planned and built, including the Possibility Playground at Hayswood Nature Reserve.', 'featured-title')}
        <ul class="row p-l0 crg-project-list mfp-gallery">
{featured}
        </ul>
        <a href="projects.html" class="crg-btn crg-btn--outline">See all projects {icon('arrow-right', 'crg-icon--md')}</a>
    </div>
</section>

<section class="section-full content-inner crg-section" aria-labelledby="process-title">
    <div class="container">
        {section_head('How we work', 'From first visit to ribbon cutting', '', 'process-title')}
        <ol class="row p-l0 crg-steps">
{steps}
        </ol>
    </div>
</section>

<section class="section-full content-inner crg-section crg-section--deep" aria-labelledby="quotes-title">
    <div class="container">
        {section_head('What our clients say', 'Trusted across Indiana', '', 'quotes-title')}
        <div class="row">
{quotes}
        </div>
    </div>
</section>

{cta()}'''

    # -------------------------------------------------------------- Products
    rows = []
    n = 0
    for p in PRODUCTS:
        if not p['photo']:
            continue
        n += 1
        points = ''.join(f'<li>{icon("check", "crg-icon--md")}<span>{x}</span></li>' for x in p['points'])
        flip = ' crg-feature--flip' if n % 2 == 0 else ''
        rows.append(f'''<article class="crg-feature{flip}" id="{p['id']}" aria-labelledby="{p['id']}-title">
            <div class="crg-feature__media"><img src="images/photos/{p['photo']}" alt="{p['alt']}" loading="lazy" width="1600" height="900"></div>
            <div class="crg-feature__body">
                <span class="crg-card__icon">{icon(p['icon'], 'crg-icon--xl')}</span>
                <h2 id="{p['id']}-title" class="crg-h2">{p['name']}</h2>
                <p class="crg-body-lg">{p['body']}</p>
                <ul class="crg-checks">{points}</ul>
            </div>
        </article>''')
    extras = []
    for p in PRODUCTS:
        if p['photo']:
            continue
        points = ''.join(f'<li>{icon("check", "crg-icon--md")}<span>{x}</span></li>' for x in p['points'])
        extras.append(f'''<div class="col-lg-4 col-md-6">
                <article class="crg-card crg-card--static" id="{p['id']}" aria-labelledby="{p['id']}-title">
                    <span class="crg-card__icon">{icon(p['icon'], 'crg-icon--xl')}</span>
                    <h2 id="{p['id']}-title" class="crg-h3">{p['name']}</h2>
                    <p>{p['body']}</p>
                    <ul class="crg-checks">{points}</ul>
                </article>
            </div>''')
    jump = ''.join(f'<li><a href="#{p["id"]}">{icon(p["icon"], "crg-icon--md")}{p["name"]}</a></li>' for p in PRODUCTS)

    products = f'''{banner('Products', 'Equipment for every play space', 'main.jpg', 'Products')}
<nav class="crg-jump" aria-label="Product categories">
    <div class="container"><ul>{jump}</ul></div>
</nav>
<section class="section-full content-inner crg-section" aria-label="Product categories">
    <div class="container crg-features">
        {''.join(rows[:2])}
    </div>
</section>
<section class="section-full content-inner crg-section crg-section--deep" aria-labelledby="more-title">
    <div class="container">
        {section_head('More from CRG', 'Surfacing, amenities &amp; more', 'Whether it’s a bench for your playground, basketball goals at your park or a full-scale renovation, we can do it.', 'more-title')}
        <div class="row">
            {''.join(extras)}
        </div>
    </div>
</section>
<section class="section-full content-inner crg-section" aria-label="Planning, design and installation">
    <div class="container crg-features">
        {''.join(rows[2:])}
    </div>
</section>
{cta('Not sure what you need?', 'Our representatives are standing by to help you design the perfect play area. Financing is available through Navitas Credit Corp.')}'''

    # -------------------------------------------------------------- Projects
    cats = [('', 'All'), ('playground', 'Playgrounds'), ('themed', 'Themed'), ('shade', 'Shade')]
    filters = '\n'.join(
        f'                <li data-filter="{c}"{" class=\"active\"" if not c else ""}><a href="#" role="button" aria-pressed="{"true" if not c else "false"}">{l}</a></li>'
        for c, l in cats)
    grid = '\n'.join(project_card(p) for p in PROJECTS)
    projects = f'''{banner('Projects', 'Play spaces we’ve built', 'crisp-wet-morning.jpg', 'Projects')}
<section class="section-full content-inner crg-section" aria-labelledby="gallery-title">
    <div class="container">
        {section_head('Gallery', 'Recent projects', 'Playgrounds, themed structures and shade. Select a photo to see it larger.', 'gallery-title')}
        <div class="site-filters crg-filters clearfix">
            <ul class="filters p-l0" aria-label="Filter projects">
{filters}
            </ul>
        </div>
        <ul id="masonry" class="dlab-gallery-listing gallery row p-l0 mfp-gallery crg-project-list">
{grid}
        </ul>
    </div>
</section>
<section class="section-full content-inner crg-section crg-section--deep" aria-labelledby="cases-title">
    <div class="container">
        {section_head('Case studies', 'Communities we’ve built for', 'The full story behind 25 projects: the site, the budget, the timeline and what our clients said. Choose one to read more.', 'cases-title')}
{h['case_grid']}
    </div>
</section>
{cta('Want a space like these?')}'''

    # ----------------------------------------------------------------- About
    values = [
        ('shield-check', 'Safety first', 'Our account reps are Certified Playground Safety Inspectors, and every install meets current safety standards.'),
        ('accessibility', 'Play for everyone', 'From the Possibility Playground in Corydon to Carey Ridge Elementary in Westfield, we build play areas kids of all abilities can use.'),
        ('handshake', 'One partner', 'Planning, design and installation of every product we offer, from one local team.'),
        ('award', 'Industry members', 'Members of the National Recreation and Park Association, based in Noblesville and installing across Indiana.'),
    ]
    vals = '\n'.join(f'''            <div class="col-lg-3 col-md-6">
                <div class="crg-card crg-card--static">
                    <span class="crg-card__icon">{icon(i, 'crg-icon--xl')}</span>
                    <h3 class="crg-h3">{t}</h3>
                        <p>{d}</p>
                </div>
            </div>''' for i, t, d in values)
    about = f'''{banner('About CRG', 'Commercial Recreation Group', 'asla-sunset.jpg', 'About')}
<section class="section-full content-inner crg-section" aria-labelledby="story-title">
    <div class="container">
        <div class="row align-items-center crg-about">
            <div class="col-lg-6">
                <p class="crg-eyebrow">Our story</p>
                <h2 id="story-title" class="crg-h1">Built for play</h2>
                <p class="crg-body-lg">We are one of the largest commercial dealers for playground equipment in the state of Indiana.</p>
                <p>Travis Goebel started with Recreation Unlimited in August 2011. With the leadership of Brad and Carey Riley, Travis helped grow its commercial division into a multi-million dollar part of the business, and his team grew from just himself to nine people, including project managers, office administrators and a full installation crew.</p>
                <p>In January 2020 the Rileys offered Travis the chance to buy the commercial division, and on March 1, 2020, Commercial Recreation Group was formed. Today we are the Indiana representative for Playcraft Systems.</p>
                <p>With 25 years of experience, we have installed hundreds of commercial products in and around Indiana. Our installation crews are some of the best in the Midwest, so you can rest assured your equipment will be installed correctly and up to current safety standards.</p>
                <ul class="crg-team">
                    <li><b>Travis Goebel</b><span>Owner</span></li>
                    <li><b>Samantha Goebel</b><span>Owner</span></li>
                    <li><b>Shane Burris</b><span>Project Manager</span></li>
                    <li><b>Nick Wolf</b><span>Project Manager</span></li>
                    <li><b>Tabitha Miller</b><span>Office Manager</span></li>
                </ul>
            </div>
            <div class="col-lg-6">
                <img class="crg-about__photo" src="images/photos/main.jpg" alt="Playground with a green spiral slide, climbing wall and rope net" loading="lazy" width="1600" height="900">
            </div>
        </div>
    </div>
</section>
<section class="section-full crg-serve" aria-labelledby="serve-title">
    <div class="container">
        <p class="crg-eyebrow">Who we serve</p>
        <h2 id="serve-title" class="crg-h1 crg-serve__statement" data-scrub-words>{SERVE}</h2>
        <ul class="crg-serve__list">
{audience_strip}
        </ul>
    </div>
</section>
<section class="section-full content-inner crg-section" aria-labelledby="values-title">
    <div class="container">
        {section_head('What we stand for', 'Why communities choose CRG', '', 'values-title')}
        <div class="row">
{vals}
        </div>
    </div>
</section>
<section class="section-full content-inner crg-section crg-section--deep" aria-labelledby="process-title">
    <div class="container">
        {section_head('How we work', 'From first visit to ribbon cutting', '', 'process-title')}
        <ol class="row p-l0 crg-steps">
{steps}
        </ol>
    </div>
</section>
{cta()}'''

    # --------------------------------------------------------------- Contact
    orgs = ['School', 'Church', 'Apartment complex', 'Daycare', 'Park / municipality', 'HOA', 'Other']
    interests = ['Play systems', 'Free-standing play', 'Shades &amp; shelters', 'Safety surfacing', 'Site amenities', 'Sports equipment', 'Dog parks', 'Not sure yet']
    timelines = ['As soon as possible', 'Within 6 months', '6–12 months', 'Over a year / budgeting']
    opt = lambda xs: ''.join(f'<option>{x}</option>' for x in xs)
    contact = f'''{banner('Contact', 'Request a quote', 'color-book-cover.jpg', 'Contact')}
<section class="section-full content-inner crg-section" aria-labelledby="quote-title">
    <div class="container">
        <div class="row">
            <div class="col-lg-4">
                <div class="crg-contact">
                    <p class="crg-eyebrow">Get in touch</p>
                    <h2 class="crg-h2">Let’s plan your play space</h2>
                    <p>Our representatives are standing by to help you design the perfect play area. Send a few details, or call us for a custom project quote.</p>
                    <ul class="crg-contact__list">
                        <li>{icon('phone')}<div><span>Phone</span><a href="tel:+13177767830">(317) 776-7830</a></div></li>
                        <li>{icon('mail')}<div><span>Email</span><a href="mailto:info@CRGplay.com">info@CRGplay.com</a></div></li>
                        <li>{icon('map-pin')}<div><span>Office</span><a href="https://www.google.com/maps/search/?api=1&amp;query=15150+Herriman+Blvd+Noblesville+IN+46060" target="_blank" rel="noopener">15150 Herriman Blvd<br>Noblesville, IN 46060</a></div></li>
                        <li>{icon('clock')}<div><span>Hours</span>Monday–Friday, 8am–5pm</div></li>
                    </ul>
                    <p class="crg-contact__note">Need financing? Our finance program through Navitas Credit Corp. offers affordable payment plans.</p>
                </div>
            </div>
            <div class="col-lg-8">
                <form class="crg-quote-form" action="script/quote.php" method="post" aria-labelledby="quote-title" data-fallback-email="info@CRGplay.com" data-fallback-phone="(317) 776-7830" novalidate>
                    <h2 id="quote-title" class="crg-h3">Quote request</h2>
                    <p class="crg-form-note">Fields marked <span aria-hidden="true">*</span><span class="sr-only">with an asterisk</span> are required.</p>
                    <div class="crg-form-grid">
                        <div class="crg-field"><label for="f-name">Name <span aria-hidden="true">*</span></label><input id="f-name" name="name" type="text" autocomplete="name" required maxlength="200"></div>
                        <div class="crg-field"><label for="f-org">Organization</label><input id="f-org" name="organization" type="text" autocomplete="organization" maxlength="200"></div>
                        <div class="crg-field"><label for="f-email">Email <span aria-hidden="true">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="200"></div>
                        <div class="crg-field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" maxlength="40"></div>
                        <div class="crg-field"><label for="f-type">Organization type</label><select id="f-type" name="org_type"><option value="">Choose one</option>{opt(orgs)}</select></div>
                        <div class="crg-field"><label for="f-interest">Interested in</label><select id="f-interest" name="interest"><option value="">Choose one</option>{opt(interests)}</select></div>
                        <div class="crg-field"><label for="f-timeline">Timeline</label><select id="f-timeline" name="timeline"><option value="">Choose one</option>{opt(timelines)}</select></div>
                        <div class="crg-field"><label for="f-city">Project city</label><input id="f-city" name="city" type="text" autocomplete="address-level2" maxlength="100"></div>
                        <div class="crg-field crg-field--full"><label for="f-message">Tell us about the project <span aria-hidden="true">*</span></label><textarea id="f-message" name="message" rows="6" required maxlength="5000" placeholder="Who will use the space, rough size, budget, anything you have in mind."></textarea></div>
                        <div class="crg-hp" aria-hidden="true"><label for="f-website">Leave this field empty</label><input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
                    </div>
                    <div class="crg-form-actions">
                        <button type="submit" class="crg-btn crg-btn--primary">Send request {icon('arrow-right', 'crg-icon--md')}</button>
                        <p class="crg-form-status" data-form-status role="status" aria-live="polite"></p>
                    </div>
                </form>
            </div>
        </div>
    </div>
</section>'''

    links = [('products.html', 'layers', 'Products', 'Play systems, shade, surfacing, sports and more.'),
             ('projects.html', 'map-pin', 'Projects', 'Case studies from schools, parks and HOAs across Indiana.'),
             ('contact.html', 'phone', 'Request a quote', 'Tell us about your project, or call (317) 776-7830.')]
    cards = '\n'.join(f'''            <div class="col-lg-4 col-md-6">
                <a class="crg-card" href="{h}">
                    <span class="crg-card__icon">{icon(i, 'crg-icon--xl')}</span>
                    <h2 class="crg-h3">{t}</h2>
                    <p>{d}</p>
                    <span class="crg-card__more">Go {icon('arrow-right', 'crg-icon--sm')}</span>
                </a>
            </div>''' for h, i, t, d in links)
    notfound = f'''{banner('Error 404', 'Page not found', 'crisp-wet-morning.jpg', 'Page not found')}
<section class="section-full content-inner crg-section" aria-labelledby="nf-title">
    <div class="container">
        <div class="crg-section-head">
            <div>
                <p class="crg-eyebrow">Let’s get you back on track</p>
                <h2 id="nf-title" class="crg-h1">This page moved or doesn’t exist</h2>
            </div>
            <p class="crg-body-lg crg-section-head__lede">Our website was recently redesigned, so older links may point to pages that have changed. Try one of these, or start from the <a href="index.html">home page</a>.</p>
        </div>
        <div class="row">
{cards}
        </div>
    </div>
</section>'''

    return [
        dict(filename='404.html', title='Page not found | CRG Commercial Recreation Group',
             desc='The page you were looking for could not be found.', body=notfound),
        dict(filename='index.html', title='CRG Commercial Recreation Group | Indiana Playground Equipment Dealer',
             desc='Commercial Recreation Group in Noblesville, IN: Playcraft playground equipment, shade, safety surfacing, sports equipment and site amenities for schools, parks, churches, daycares, apartments and HOAs. Call (317) 776-7830.', body=home),
        dict(filename='products.html', title='Products | CRG Commercial Recreation Group',
             desc='Playcraft play systems, free-standing play, shades and shelters, safety surfacing, site amenities, sports equipment, dog parks, and planning, design and installation.', body=products),
        dict(filename='projects.html', title='Projects | CRG Commercial Recreation Group',
             desc='Playgrounds and case studies by Commercial Recreation Group, including the Possibility Playground at Hayswood Nature Reserve.', body=projects),
        dict(filename='about.html', title='About | CRG Commercial Recreation Group',
             desc='Commercial Recreation Group in Noblesville, IN: 25 years of experience and one of the largest commercial playground equipment dealers in Indiana.', body=about),
        dict(filename='contact.html', title='Request a Quote | CRG Commercial Recreation Group',
             desc='Request a quote from Commercial Recreation Group. Call (317) 776-7830 or email info@CRGplay.com.', body=contact,
             extra_scripts='\n<script src="js/quote-form.js"></script>'),
    ]
