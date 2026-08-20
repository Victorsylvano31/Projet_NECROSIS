import ldap3
import time

class ADCollector:
    def __init__(self, config):
        self.config = config

    def collect(self):
        results = {"users": [], "groups": [], "computers": [], "error": None}
        try:
            server = ldap3.Server(self.config.target_domain, get_info=ldap3.ALL)
            conn = ldap3.Connection(
                server,
                user=self.config.user,
                password=self.config.password,
                authentication=ldap3.NTLM,
                auto_bind=True
            )
            base = f"DC={self.config.target_domain.split('.')[0]},DC={self.config.target_domain.split('.')[1]}"
            
            # Utilisateurs
            conn.search(
                search_base=base,
                search_filter='(objectClass=user)',
                attributes=['sAMAccountName', 'displayName', 'mail', 'pwdLastSet', 'whenCreated', 'givenName', 'sn', 'department', 'title']
            )
            for entry in conn.entries:
                results["users"].append({
                    "sAMAccountName": str(entry.sAMAccountName) if hasattr(entry, 'sAMAccountName') else "",
                    "displayName": str(entry.displayName) if hasattr(entry, 'displayName') else "",
                    "mail": str(entry.mail) if hasattr(entry, 'mail') else "",
                    "givenName": str(entry.givenName) if hasattr(entry, 'givenName') else "",
                    "sn": str(entry.sn) if hasattr(entry, 'sn') else "",
                    "department": str(entry.department) if hasattr(entry, 'department') else ""
                })
            
            # Groupes
            conn.search(base, '(objectClass=group)', attributes=['cn', 'description', 'member'])
            for entry in conn.entries:
                results["groups"].append({
                    "cn": str(entry.cn) if hasattr(entry, 'cn') else "",
                    "members_count": len(entry.member) if hasattr(entry, 'member') else 0
                })
            
            # Ordinateurs
            conn.search(base, '(objectClass=computer)', attributes=['name', 'operatingSystem', 'dNSHostName'])
            for entry in conn.entries:
                results["computers"].append({
                    "name": str(entry.name) if hasattr(entry, 'name') else "",
                    "os": str(entry.operatingSystem) if hasattr(entry, 'operatingSystem') else ""
                })
            
            conn.unbind()
        except Exception as e:
            results["error"] = str(e)
        return results