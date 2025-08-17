# Written Information Security Program (WISP)

This document outlines data security and compliance practices for **TaxCRM**.

## 1. Data Protection
- All client data encrypted in transit (HTTPS/TLS) and at rest (AWS S3 + KMS).
- Access controlled via IAM roles and OAuth2 authentication.

## 2. Vendors
- AWS (S3, Lambda, CloudWatch).
- DocuSign/HelloSign (e-signatures).
- Stripe (billing).

## 3. Logging & Monitoring
- Audit logging of API access.
- CloudWatch alerts for suspicious activity.

## 4. Compliance
- IRS Pub 4557 (Safeguarding Taxpayer Data).
- FTC Safeguards Rule.
- GDPR/CCPA readiness for personal data.

## 5. Incident Response
- Security incidents logged and reported within 24 hours.
- Breach notifications in compliance with IRS & FTC requirements.
