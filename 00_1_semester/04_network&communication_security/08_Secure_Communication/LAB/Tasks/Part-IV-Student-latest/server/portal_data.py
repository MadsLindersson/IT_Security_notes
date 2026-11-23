"""Entirely fictional records for the two networking-lab accounts."""
STUDENTS = {
    'alice': {
        'name': 'Alice Jensen', 'first_name': 'Alice', 'initials': 'AJ',
        'student_id': 'STU-2026-1042', 'programme': 'Cybersecurity Services',
        'semester': 'Security Operations', 'status': 'Active',
        'email': 'alice.student@example.test', 'attendance': 92,
        'classes': [
            ('MON', '07', '09:00–10:30', 'Network Security Review', 'Team meeting · Room N2.04'),
            ('TUE', '08', '10:45–12:15', 'Client Security Briefing', 'Project meeting · Room N1.12'),
            ('THU', '10', '13:00–14:30', 'Systems Security Review', 'Team workshop · Room N2.08'),
        ],
        'grades': [('Network assessments', '10'), ('Linux system reviews', '12'), ('Security assessments', '7')],
        'notifications': [
            ('Updated incident response resources', 'Network Security Review · Today'),
            ('Weekly client report due Friday', 'Submit your report before 16:00 · Yesterday'),
            ('Thursday meeting room update', 'Systems Security Review moves to N2.08 · 4 Sep'),
        ],
    },
    'bob': {
        'name': 'Bob Nielsen', 'first_name': 'Bob', 'initials': 'BN',
        'student_id': 'STU-2026-1088', 'programme': 'Cybersecurity Services',
        'semester': 'Security Operations', 'status': 'Active',
        'email': 'bob.student@example.test', 'attendance': 86,
        'classes': [
            ('MON', '07', '10:45–12:15', 'Systems Security Review', 'Project meeting · Room N1.06'),
            ('WED', '09', '09:00–10:30', 'Secure Software Review', 'Team meeting · Room N2.02'),
            ('THU', '10', '13:00–14:30', 'Network Security Review', 'Team workshop · Room N1.12'),
        ],
        'grades': [('Network assessments', '7'), ('Linux system reviews', '10'), ('Code security reviews', '10')],
        'notifications': [
            ('Client project team confirmed', 'Your team is ready for the next workshop · Today'),
            ('Updated engineering resources', 'Secure Software Review · Yesterday'),
            ('Security review preparation', 'Review the network assessment before Thursday · 4 Sep'),
        ],
    },
}
