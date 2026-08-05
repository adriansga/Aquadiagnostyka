const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS || 'https://aquadiagnostyka.pl,https://www.aquadiagnostyka.pl')
  .split(',')
  .map(origin => origin.trim())
  .filter(Boolean);

function setCors(req, res) {
  const origin = req.headers.origin || '';
  const allowedOrigin = ALLOWED_ORIGINS.includes(origin)
    || /^https:\/\/[a-z0-9-]+\.vercel\.app$/i.test(origin)
    || /^http:\/\/(localhost|127\.0\.0\.1):\d+$/i.test(origin)
    ? origin
    : 'https://aquadiagnostyka.pl';

  res.setHeader('Access-Control-Allow-Origin', allowedOrigin);
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(body));
}

function clean(value, limit = 500) {
  return String(value || '')
    .replace(/[\u0000-\u001F\u007F]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, limit);
}

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value || '').trim());
}

function escapeHtml(value) {
  return clean(value, 5000)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function listFromSemicolon(value) {
  return clean(value, 4000)
    .split(';')
    .map(item => item.trim())
    .filter(Boolean);
}

function firstValue(payload, names, limit = 220) {
  for (const name of names) {
    const value = clean(payload[name], limit);
    if (value) return value;
  }
  return '';
}

function adminRecipients() {
  return (process.env.ADMIN_TO || 'awielochapv@gmail.com')
    .split(',')
    .map(item => item.trim())
    .filter(Boolean);
}

function leadTitle(payload, email) {
  return firstValue(payload, ['imie_nazwisko', 'name', 'nazwisko'], 160)
    || firstValue(payload, ['telefon', 'phone'], 80)
    || email
    || 'bez danych';
}

function leadRows(payload) {
  const rows = [
    ['Imię i nazwisko', firstValue(payload, ['imie_nazwisko', 'name', 'nazwisko'], 180)],
    ['Telefon', firstValue(payload, ['telefon', 'phone'], 80)],
    ['Email', firstValue(payload, ['email'], 220)],
    ['Adres pobrania', firstValue(payload, ['adres', 'adres_pobrania'], 260)],
    ['Adres wysyłki', firstValue(payload, ['adres_wysylki'], 260)],
    ['Produkt', firstValue(payload, ['produkt', 'pakiet_nazwa'], 260)],
    ['Zakres / pakiet', firstValue(payload, ['pakiet_parametry', 'liczba_zestawow'], 4000)],
    ['Cena brutto', firstValue(payload, ['pakiet_cena_brutto', 'diy_suma_brutto'], 120)],
    ['Rabat', firstValue(payload, ['pakiet_rabat_kwota'], 120)],
    ['Kod rabatu', firstValue(payload, ['pakiet_kod_rabatu'], 120)],
    ['Uwagi', firstValue(payload, ['uwagi', 'message'], 900)],
    ['Źródło', firstValue(payload, ['zrodlo', 'source_kind'], 220)],
    ['Landing URL', firstValue(payload, ['landing_url'], 900)],
    ['Pierwszy landing', firstValue(payload, ['first_landing_url'], 900)],
    ['UTM source', firstValue(payload, ['utm_source'], 160)],
    ['UTM medium', firstValue(payload, ['utm_medium'], 160)],
    ['UTM campaign', firstValue(payload, ['utm_campaign'], 180)],
    ['GCLID', firstValue(payload, ['gclid'], 220)],
    ['Session ID', firstValue(payload, ['session_id'], 120)]
  ];

  return rows.filter(([, value]) => value);
}

function buildAdminHtml(payload, email) {
  const rows = leadRows(payload);
  const htmlRows = rows.map(([label, value]) => `
          <tr>
            <td style="padding:8px 10px;border-bottom:1px solid #dbeaf0;color:#5d7280;width:165px;vertical-align:top;">${escapeHtml(label)}</td>
            <td style="padding:8px 10px;border-bottom:1px solid #dbeaf0;color:#102532;vertical-align:top;">${escapeHtml(value)}</td>
          </tr>`).join('');

  return `<!doctype html>
<html lang="pl">
  <body style="margin:0;background:#f4fafc;color:#102532;font-family:Arial,sans-serif;line-height:1.55;">
    <div style="max-width:760px;margin:0 auto;padding:24px 16px;">
      <div style="background:#ffffff;border:1px solid #dbeaf0;border-radius:14px;padding:24px;">
        <p style="margin:0 0 8px;color:#147fa8;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;">AquaDiagnostyka - nowe zlecenie</p>
        <h1 style="margin:0 0 14px;font-size:22px;line-height:1.2;color:#102532;">Nowe zgłoszenie z formularza</h1>
        <p style="margin:0 0 16px;">Formspree przyjęło formularz, a ten mail jest niezależnym powiadomieniem admina z endpointu Resend.</p>
        <table cellspacing="0" cellpadding="0" style="width:100%;border-collapse:collapse;background:#fbfdfe;border:1px solid #dbeaf0;border-radius:10px;overflow:hidden;">
          ${htmlRows || '<tr><td style="padding:10px;">Brak pól formularza.</td></tr>'}
        </table>
        <p style="margin-top:18px;">Odpowiedz na tego maila, żeby napisać bezpośrednio do klienta: <strong>${escapeHtml(email)}</strong>.</p>
      </div>
    </div>
  </body>
</html>`;
}

function buildAdminText(payload, email) {
  const lines = [
    'AquaDiagnostyka - nowe zlecenie z formularza',
    '',
    'Formspree przyjęło formularz, a ten mail jest niezależnym powiadomieniem admina z endpointu Resend.',
    ''
  ];

  for (const [label, value] of leadRows(payload)) {
    lines.push(`${label}: ${value}`);
  }

  lines.push('', `Odpowiedz na tego maila, żeby napisać bezpośrednio do klienta: ${email}`);
  return lines.join('\n');
}

async function sendResendMail(mail) {
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
      'User-Agent': 'AquaDiagnostykaConfirmation/1.1'
    },
    body: JSON.stringify(mail)
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const error = new Error('resend_error');
    error.status = response.status;
    error.details = data && data.name ? data.name : 'unknown';
    throw error;
  }

  return data;
}

async function fetchEmailStatus(id) {
  if (!id) return null;

  try {
    const response = await fetch(`https://api.resend.com/emails/${encodeURIComponent(id)}`, {
      headers: {
        Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
        'User-Agent': 'AquaDiagnostykaConfirmation/1.1'
      }
    });

    if (!response.ok) return null;
    const data = await response.json().catch(() => ({}));
    return data && data.last_event ? data.last_event : null;
  } catch (error) {
    return null;
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function waitForEmailStatus(id) {
  for (const delay of [900, 1600, 2600]) {
    await sleep(delay);
    const status = await fetchEmailStatus(id);
    if (status) return status;
  }
  return null;
}

function buildHtml(payload) {
  const selected = listFromSemicolon(payload.pakiet_parametry);
  const total = clean(payload.pakiet_cena_brutto, 80) || 'do potwierdzenia';
  const original = clean(payload.pakiet_cena_przed_rabatem, 80);
  const discount = clean(payload.pakiet_rabat_kwota, 80);
  const discountCode = clean(payload.pakiet_kod_rabatu, 120);
  const diyInterest = clean(payload.diy_zainteresowanie, 120);
  const diyVariant = clean(payload.diy_wariant, 180);
  const diyQty = clean(payload.diy_ilosc, 40);
  const diyTotal = clean(payload.diy_suma_brutto, 80);
  const address = clean(payload.adres, 220);
  const notes = clean(payload.uwagi, 600);

  const selectedHtml = selected.length
    ? `<ul>${selected.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`
    : '<p>Zakres badania zostanie potwierdzony po kontakcie.</p>';

  const discountHtml = discountCode
    ? `<p><strong>Rabat:</strong> ${escapeHtml(discount || '-')} (${escapeHtml(discountCode)})<br><strong>Kwota przed rabatem:</strong> ${escapeHtml(original || '-')}</p>`
    : '';

  const diyHtml = diyInterest
    ? `<p><strong>Zestaw DIY:</strong> ${escapeHtml(diyVariant || diyInterest)}<br><strong>Ilość:</strong> ${escapeHtml(diyQty || '1')}<br><strong>Suma DIY z dostawą:</strong> ${escapeHtml(diyTotal || 'do potwierdzenia')}</p>`
    : '';

  return `<!doctype html>
<html lang="pl">
  <body style="margin:0;background:#f4fafc;color:#102532;font-family:Arial,sans-serif;line-height:1.55;">
    <div style="max-width:640px;margin:0 auto;padding:28px 16px;">
      <div style="background:#ffffff;border:1px solid #dbeaf0;border-radius:14px;padding:26px;">
        <p style="margin:0 0 8px;color:#147fa8;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;">AquaDiagnostyka</p>
        <h1 style="margin:0 0 16px;font-size:24px;line-height:1.2;color:#102532;">Otrzymaliśmy zgłoszenie badania wody</h1>
        <p>Dzień dobry,</p>
        <p>dziękujemy za wysłanie zgłoszenia. Poniżej zapisaliśmy zakres i kwotę z formularza. To nie jest jeszcze płatność ani potwierdzony termin - odezwiemy się, żeby potwierdzić szczegóły pobrania próbki.</p>
        <div style="background:#f4fafc;border:1px solid #dbeaf0;border-radius:12px;padding:16px;margin:18px 0;">
          <p style="margin:0 0 8px;"><strong>Wybrany zakres:</strong></p>
          ${selectedHtml}
          <p><strong>Kwota brutto z formularza:</strong> ${escapeHtml(total)}</p>
          ${discountHtml}
          ${diyHtml}
          ${address ? `<p><strong>Adres pobrania próbki:</strong> ${escapeHtml(address)}</p>` : ''}
          ${notes ? `<p><strong>Uwagi:</strong> ${escapeHtml(notes)}</p>` : ''}
        </div>
        <p>W następnym kroku potwierdzimy zakres badania, termin oraz sposób pobrania próbki. W razie pomyłki możesz odpisać bezpośrednio na tę wiadomość.</p>
        <p style="margin-top:24px;">Zespół AquaDiagnostyka<br><a href="mailto:kontakt@aquadiagnostyka.pl" style="color:#147fa8;">kontakt@aquadiagnostyka.pl</a></p>
      </div>
      <p style="margin:14px 0 0;color:#6b7d88;font-size:12px;text-align:center;">Ta wiadomość została wysłana automatycznie po złożeniu formularza na aquadiagnostyka.pl.</p>
    </div>
  </body>
</html>`;
}

function buildText(payload) {
  const lines = [
    'AquaDiagnostyka - potwierdzenie zgłoszenia',
    '',
    'Dzień dobry,',
    'dziękujemy za wysłanie zgłoszenia. Poniżej zapisaliśmy zakres i kwotę z formularza.',
    'To nie jest jeszcze płatność ani potwierdzony termin - odezwiemy się, żeby potwierdzić szczegóły pobrania próbki.',
    '',
    `Wybrany zakres: ${clean(payload.pakiet_parametry, 4000) || 'do potwierdzenia'}`,
    `Kwota brutto z formularza: ${clean(payload.pakiet_cena_brutto, 80) || 'do potwierdzenia'}`
  ];

  if (clean(payload.pakiet_kod_rabatu, 120)) {
    lines.push(`Rabat: ${clean(payload.pakiet_rabat_kwota, 80)} (${clean(payload.pakiet_kod_rabatu, 120)})`);
    lines.push(`Kwota przed rabatem: ${clean(payload.pakiet_cena_przed_rabatem, 80)}`);
  }

  if (clean(payload.diy_zainteresowanie, 120)) {
    lines.push(`Zestaw DIY: ${clean(payload.diy_wariant, 180) || clean(payload.diy_zainteresowanie, 120)}`);
    lines.push(`Ilość DIY: ${clean(payload.diy_ilosc, 40) || '1'}`);
    lines.push(`Suma DIY z dostawą: ${clean(payload.diy_suma_brutto, 80) || 'do potwierdzenia'}`);
  }

  if (clean(payload.adres, 220)) lines.push(`Adres pobrania próbki: ${clean(payload.adres, 220)}`);
  if (clean(payload.uwagi, 600)) lines.push(`Uwagi: ${clean(payload.uwagi, 600)}`);

  lines.push('', 'W razie pomyłki możesz odpisać bezpośrednio na tę wiadomość.', '', 'Zespół AquaDiagnostyka', 'kontakt@aquadiagnostyka.pl');
  return lines.join('\n');
}

module.exports = async function handler(req, res) {
  setCors(req, res);

  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    res.end();
    return;
  }

  if (req.method !== 'POST') {
    json(res, 405, { ok: false, error: 'method_not_allowed' });
    return;
  }

  const payload = typeof req.body === 'object' && req.body ? req.body : {};
  const email = clean(payload.email, 220).toLowerCase();

  if (!isEmail(email)) {
    json(res, 400, { ok: false, error: 'invalid_email' });
    return;
  }

  if (!process.env.RESEND_API_KEY) {
    json(res, 500, { ok: false, error: 'missing_resend_key' });
    return;
  }

  const mail = {
    from: process.env.MAIL_FROM || 'Zespół AquaDiagnostyka <kontakt@aquadiagnostyka.pl>',
    to: [email],
    reply_to: process.env.MAIL_REPLY_TO || 'kontakt@aquadiagnostyka.pl',
    subject: 'Potwierdzenie zgłoszenia - AquaDiagnostyka',
    html: buildHtml(payload),
    text: buildText(payload)
  };

  try {
    const data = await sendResendMail(mail);
    const customerId = data.id || null;
    let admin = { ok: false, id: null, last_event: null };

    try {
      const title = leadTitle(payload, email);
      const adminMail = {
        from: process.env.MAIL_FROM || 'Zespół AquaDiagnostyka <kontakt@aquadiagnostyka.pl>',
        to: adminRecipients(),
        reply_to: email,
        subject: `NOWE ZLECENIE - AquaDiagnostyka - ${title}`,
        html: buildAdminHtml(payload, email),
        text: buildAdminText(payload, email)
      };
      const adminData = await sendResendMail(adminMail);
      admin = {
        ok: true,
        id: adminData.id || null,
        last_event: await waitForEmailStatus(adminData.id || null)
      };
    } catch (adminError) {
      admin = {
        ok: false,
        id: null,
        error: adminError.message || 'admin_send_failed',
        status: adminError.status || null,
        details: adminError.details || null
      };
    }

    json(res, 200, { ok: true, id: customerId, admin });
  } catch (error) {
    json(res, 502, {
      ok: false,
      error: error.message === 'resend_error' ? 'resend_error' : 'send_failed',
      status: error.status || null,
      details: error.details || null
    });
  }
};
