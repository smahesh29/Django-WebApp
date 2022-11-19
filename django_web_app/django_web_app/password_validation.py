from django.forms import ValidationError
from password_strength import PasswordStats

class PasswordVerifier:
    passwordsettings = {
        'minlength': 14,
        'maxlength': 20,
        'mindigits': 1,
        'maxorderedsequencelen': 3,
        'maxrepeatedpatternlen': 3,
        'mindictwordlen': 3,
        'minentropybits': 1,
        'minlowercaseletters': 1,
        'minuppercaseletters': 1,
        'minspecialcharacters': 1,
        'forceminlength': True,
        'forcemaxlength': True,
        'forcemindigits': True,
        'forcemaxorderedsequencelen': False,
        'forcemaxrepeatedpatternlen': False,
        'forcemindictwordlen': True,
        'forceminentropybits': False,
        'forceminlowercaseletters': True,
        'forceminuppercaseletters': True,
        'forceminspecialcharacters': True
    }

    def verify(self, password):
        output = {}
        stats = PasswordStats(password)
        output.update(self.checkrules(stats))
        return output

    def checkrules(self, stats):
        output = {}
        if self.passwordsettings.get('forceminlength', False) and \
           stats.length < self.passwordsettings['minlength']:
            output['tooshort'] = True
        if self.passwordsettings.get('forcemaxlength', False) and \
           stats.length > self.passwordsettings['maxlength']:
            output['toolong'] = True
        if self.passwordsettings.get('forceminentropybits', False) and \
           stats.entropy_bits < self.passwordsettings['minentropybits']:
            output['notenoughentropybits'] = True
        if self.passwordsettings.get('forcemaxorderedsequencelen', False) and \
           stats.sequences_length > self.passwordsettings['maxorderedsequencelen']:
            output['toolongseq'] = True
        if self.passwordsettings.get('forcemaxrepeatedpatternlen', False) and \
           stats.repeated_patterns_length > self.passwordsettings['maxrepeatedpatternlen']:
            output['repeatedpattern'] = True
        if self.passwordsettings.get('forcemindigits', False) and \
           stats.numbers < self.passwordsettings['mindigits']:
            output['numbers'] = True
        if self.passwordsettings.get('forceminlowercaseletters', False) and \
           stats.letters_lowercase < self.passwordsettings['minlowercaseletters']:
            output['lowercase'] = True
        if self.passwordsettings.get('forceminuppercaseletters', False) and \
           stats.letters_uppercase < self.passwordsettings['minuppercaseletters']:
            output['uppercase'] = True
        if self.passwordsettings.get('forceminspecialcharacters', False) and \
           stats.special_characters < self.passwordsettings['minspecialcharacters']:
            output['special'] = True
        return output


class CustomPasswordValidator:

    def validate(self, password, userid=None):
        print("CustomPasswordValidator: ", password)
        results = PasswordVerifier().verify(password=password)
        matchedwords = results.get('matchedwords', '')

        errorsmessages = {
            'numbers': 'Password does not have enough digits',
            'repeatedpattern': 'Password has too long repeated pattern',
            'dictionaryword': 'Password has forbidden words: ' + ', '.join(matchedwords),
            'toolongseq': 'Password has too long sequence',
            'notenoughentropybits': 'Password does not have enough entropy bits',
            'toolong': 'Password is too long',
            'tooshort': 'Password is too short',
            'lowercase': 'Password does not have enough lowercase letters',
            'uppercase': 'Password does not have enough uppercase letters',
            'special': 'Password does not have enough special characters',
        }

        errors = set(errorsmessages.keys()).intersection(results)

        printederrors = [errorsmessages[key] for key in errors]
        if errors:
            raise ValidationError(
                printederrors
            )

    def get_help_text(self):
        """Required method see link above"""
        return "Use strong password"
