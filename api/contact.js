const { Resend } = require('resend');

const resend = new Resend(process.env.RESEND_API_KEY);
const TO_EMAIL = process.env.CONTACT_EMAIL || 'wilsonandreina@yahoo.com';
const FROM_EMAIL = 'Makeup & Hair by Andreina <noreply@makeupandhairbyandreina.com>';

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  let body;
  try {
    body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
  } catch {
    return res.status(400).json({ error: 'Invalid request.' });
  }

  const { firstName, lastName, email, phone, eventType, eventDate, location, partySize, message } = body || {};

  if (!firstName?.trim() || !email?.trim()) {
    return res.status(400).json({ error: 'Name and email are required.' });
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ error: 'Please enter a valid email address.' });
  }

  const name = [firstName.trim(), lastName?.trim()].filter(Boolean).join(' ');

  try {
    await resend.emails.send({
      from: FROM_EMAIL,
      to: TO_EMAIL,
      replyTo: email.trim(),
      subject: `New Inquiry — ${name} · ${eventType || 'General'}`,
      text: `
New inquiry from makeupandhairbyandreina.com

Name: ${name}
Email: ${email.trim()}
Phone: ${phone || 'Not provided'}
Event Type: ${eventType || 'Not provided'}
Event Date: ${eventDate || 'Not provided'}
Location: ${location || 'Not provided'}
Party Size: ${partySize || 'Not provided'}

Message:
${message || 'No message provided'}
      `.trim(),
      html: `
<div style="font-family:Georgia,serif;max-width:600px;margin:0 auto;color:#1E1218;">
  <div style="background:#F2DDD8;padding:32px;border-top:3px solid #C8A06A;">
    <h1 style="font-size:22px;font-weight:400;margin:0 0 6px;">New Booking Inquiry</h1>
    <p style="font-size:12px;color:#888;margin:0;font-family:Arial,sans-serif;">from makeupandhairbyandreina.com</p>
  </div>
  <div style="padding:32px;background:#fff;">
    <table style="width:100%;font-family:Arial,sans-serif;font-size:14px;border-collapse:collapse;">
      <tr><td style="padding:8px 0;color:#888;width:140px;">Name</td><td style="padding:8px 0;font-weight:500;">${name}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Email</td><td style="padding:8px 0;"><a href="mailto:${email.trim()}" style="color:#C8A06A;">${email.trim()}</a></td></tr>
      <tr><td style="padding:8px 0;color:#888;">Phone</td><td style="padding:8px 0;">${phone || 'Not provided'}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Event Type</td><td style="padding:8px 0;">${eventType || 'Not provided'}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Event Date</td><td style="padding:8px 0;">${eventDate || 'Not provided'}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Location</td><td style="padding:8px 0;">${location || 'Not provided'}</td></tr>
      <tr><td style="padding:8px 0;color:#888;">Party Size</td><td style="padding:8px 0;">${partySize || 'Not provided'}</td></tr>
    </table>
    ${message ? `
    <div style="margin-top:24px;padding-top:24px;border-top:1px solid #eee;">
      <p style="font-size:12px;color:#888;font-family:Arial,sans-serif;margin:0 0 8px;text-transform:uppercase;letter-spacing:1px;">Message</p>
      <p style="font-family:Arial,sans-serif;font-size:14px;line-height:1.6;margin:0;">${message}</p>
    </div>` : ''}
  </div>
  <div style="padding:16px 32px;background:#F2DDD8;font-family:Arial,sans-serif;font-size:12px;color:#aaa;">
    Makeup &amp; Hair by Andreina &nbsp;·&nbsp; Rockwall, TX
  </div>
</div>
      `.trim(),
    });

    // Confirmation to submitter — swallow errors so a delivery failure doesn't surface as a form error
    resend.emails.send({
      from: FROM_EMAIL,
      to: email.trim(),
      replyTo: TO_EMAIL,
      subject: 'Your inquiry was received — Makeup & Hair by Andreina',
      text: `
Hi ${firstName.trim()},

Thank you for reaching out! I've received your inquiry and will get back to you within 2 business days to check availability and discuss your event.

In the meantime, feel free to browse my gallery or follow along on Instagram @makeupandhairbyandreinallc.

With love,
Andreina
Makeup & Hair by Andreina · Rockwall, TX
wilsonandreina@yahoo.com | (956) 640-6220
      `.trim(),
      html: `
<div style="font-family:Georgia,serif;max-width:600px;margin:0 auto;color:#1E1218;">
  <div style="background:#F2DDD8;padding:32px;border-top:3px solid #C8A06A;">
    <h1 style="font-size:22px;font-weight:400;margin:0 0 4px;">Thank you, ${firstName.trim()}!</h1>
    <p style="font-size:13px;color:#888;margin:0;font-family:Arial,sans-serif;">Makeup &amp; Hair by Andreina &nbsp;·&nbsp; Rockwall, TX</p>
  </div>
  <div style="padding:32px;background:#fff;font-family:Arial,sans-serif;font-size:14px;line-height:1.7;color:#444;">
    <p>I've received your inquiry and will be in touch within <strong>2 business days</strong> to check availability and discuss your event.</p>
    <p>In the meantime, feel free to browse my gallery or follow along on Instagram for the latest looks and behind-the-scenes moments.</p>
    <p style="margin-top:32px;">
      <a href="https://www.instagram.com/makeupandhairbyandreinallc" style="color:#C8A06A;text-decoration:none;">@makeupandhairbyandreinallc on Instagram</a>
    </p>
  </div>
  <div style="padding:16px 32px;background:#F2DDD8;font-family:Arial,sans-serif;font-size:12px;color:#aaa;">
    With love, Andreina &nbsp;·&nbsp; <a href="mailto:wilsonandreina@yahoo.com" style="color:#aaa;">wilsonandreina@yahoo.com</a> &nbsp;·&nbsp; (956) 640-6220
  </div>
</div>
      `.trim(),
    });

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('Contact form error:', err);
    return res.status(500).json({ error: 'Something went wrong. Please email or call directly.' });
  }
};
