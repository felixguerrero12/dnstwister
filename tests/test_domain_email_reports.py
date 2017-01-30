"""Tests of the email report view model."""
import datetime

from dnstwister.domain.email_report import EmailReport


def test_noisy_flags_separates_domains_in_report():
    """Tests domains with the noisy flag set are ."""
    new = (
        ('www.example1.com', '127.0.0.1'),
        ('www.example7.com', '127.0.0.9'),
    )
    updated = (
        ('www.example2.com', '127.0.0.1', '127.0.0.2'),
        ('www.example9.com', '127.0.0.3', '127.0.0.4'),
    )
    deleted = (
        'www.example3.com',
        'www.example15.com',
    )
    noisy = set(
        ('www.example7.com', 'www.example2.com', 'www.example3.com')
    )

    report = EmailReport(new, updated, deleted, noisy)

    assert report.alertable['new'] == [('www.example1.com', '127.0.0.1')]
    assert report.alertable['updated'] == [('www.example9.com', '127.0.0.3', '127.0.0.4')]
    assert report.alertable['deleted'] == ['www.example15.com']

    assert report.noisy['new'] == [('www.example7.com', '127.0.0.9')]
    assert report.noisy['updated'] == [('www.example2.com', '127.0.0.1', '127.0.0.2')]
    assert report.noisy['deleted'] == ['www.example3.com']