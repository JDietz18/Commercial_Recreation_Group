<?php
/*
 * CRG quote request handler.
 *
 * Replaces Intera's script/contact.php. Posted to by js/quote-form.js and
 * answers with JSON: {"status": 1|0, "msg": "..."}.
 *
 * Configure the three settings below before launch.
 */

/* Where quote requests are delivered. */
const CRG_QUOTE_TO = 'info@CRGplay.com';

/* Sender address. Must be on a domain your mail server may send for,
   or messages will land in spam. Replies go to the visitor via Reply-To. */
const CRG_QUOTE_FROM = 'website@crgplay.com'; // TODO: confirm this address exists on crgplay.com's mail server

/* Optional Google reCAPTCHA v2 secret. Leave empty to rely on the honeypot
   field only. If set, also set data-sitekey in contact.html. */
const CRG_RECAPTCHA_SECRET = '';

header('Content-Type: application/json; charset=utf-8');

function respond(int $status, string $msg): void
{
    echo json_encode(['status' => $status, 'msg' => $msg]);
    exit;
}

function field(string $name, int $max = 200): string
{
    $value = isset($_POST[$name]) && is_string($_POST[$name]) ? trim($_POST[$name]) : '';
    $value = str_replace(["\r", "\0"], '', $value);
    return mb_substr($value, 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    respond(0, 'Method not allowed.');
}

/* Honeypot: real visitors never see or fill this field. */
if (field('website') !== '') {
    respond(1, 'Thanks! We received your request and will be in touch soon.');
}

if (CRG_RECAPTCHA_SECRET !== '') {
    require __DIR__ . '/recaptcha-master/src/autoload.php';
    $recaptcha = new \ReCaptcha\ReCaptcha(CRG_RECAPTCHA_SECRET, new \ReCaptcha\RequestMethod\CurlPost());
    $check = $recaptcha->verify(field('g-recaptcha-response', 4000), $_SERVER['REMOTE_ADDR'] ?? '');
    if (!$check->isSuccess()) {
        respond(0, 'Please complete the "I\'m not a robot" check and try again.');
    }
}

$fields = [
    'Name'          => field('name'),
    'Organization'  => field('organization'),
    'Email'         => field('email'),
    'Phone'         => field('phone', 40),
    'Organization type' => field('org_type', 60),
    'Interested in' => field('interest', 60),
    'Timeline'      => field('timeline', 60),
    'Project city'  => field('city', 100),
    'Message'       => field('message', 5000),
];

if ($fields['Name'] === '' || $fields['Email'] === '' || $fields['Message'] === '') {
    respond(0, 'Please fill in your name, email and a few details about the project.');
}
if (!filter_var($fields['Email'], FILTER_VALIDATE_EMAIL)) {
    respond(0, 'That email address doesn\'t look right. Please check it and try again.');
}

$rows = '';
foreach ($fields as $label => $value) {
    if ($value === '') {
        continue;
    }
    $rows .= '<tr><th align="left" valign="top" style="padding:4px 12px 4px 0">'
        . htmlspecialchars($label, ENT_QUOTES, 'UTF-8') . '</th><td style="padding:4px 0">'
        . nl2br(htmlspecialchars($value, ENT_QUOTES, 'UTF-8')) . '</td></tr>';
}

$subject = 'Quote request: ' . ($fields['Organization'] !== '' ? $fields['Organization'] : $fields['Name']);
$subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
$body = '<p>New quote request from the CRG website.</p><table>' . $rows . '</table>';

$headers = implode("\r\n", [
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8',
    'From: CRG Website <' . CRG_QUOTE_FROM . '>',
    'Reply-To: ' . $fields['Email'],
]);

if (mail(CRG_QUOTE_TO, $subject, $body, $headers)) {
    respond(1, 'Thanks! We received your request and will be in touch soon.');
}
respond(0, 'Sorry, your request could not be sent. Please try again, or call or email us directly.');
