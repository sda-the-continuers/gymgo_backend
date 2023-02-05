

class JWTAccountInterface:

    jwt_claim_keys = []

    def get_jwt_claim_keys(self):
        return self.jwt_claim_keys

    def get_jwt_claims(self):
        claims = dict()
        for claim_key in set(self.jwt_claim_keys):
            if isinstance(claim_key, (tuple, list)) and len(claim_key) == 2:
                field_name, claim_key = claim_key
            elif isinstance(claim_key, str):
                field_name, claim_key = claim_key, claim_key
            else:
                raise ValueError('claim key must be a <field_name, claim_key> tuple or an instance of str')
            claims[claim_key] = getattr(self, field_name)
        return claims
