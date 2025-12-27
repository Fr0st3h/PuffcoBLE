

class PuffcoUtils:
    def revision_number_to_string(value):
        rev_letters = 'ABCDEFGHJKMNPRTUVWXYZ'
        if not isinstance(value, int) or value < 0:
            return str(value)
        if value == 0:
            return 'X*'
        shift = value - 1
        out = ''
        while shift >= 0:
            out = rev_letters[shift % len(rev_letters)] + out
            shift = shift // len(rev_letters) - 1
        return out