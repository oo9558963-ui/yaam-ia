# YAAM IA BF - Version Hors-ligne Intelligente comme Meta AI 🇧🇫
# Marche sans internet sur ton PC à Ouaga

def yaam_intelligente():
    print("="*50)
    print("YAAM IA BF 🇧🇫 est en ligne (hors-ligne)")
    print("Je parle Français, Mooré, Dioula - comme Meta AI")
    print("Tape 'quitter' pour sortir")
    print("="*50)
    
    produits = {
        "crème lèvre rose": {"prix": "3000F", "stock": "Disponible", "desc": "Pour lèvres douces et roses, naturel"},
        "faso dan fani": {"prix": "15000F", "stock": "Sur commande", "desc": "Authentique du Burkina"}
    }
    
    while True:
        user = input("\nToi: ").strip()
        if not user: continue
        lower = user.lower()
        
        if lower in ["quitter", "exit", "bye"]:
            print("YAAM: N yita anoure ! À bientôt à Ouaga ! 👋")
            break
        
        # Intelligence - Mooré
        elif "yibeogo" in lower or "ne y" in lower or "laafi" in lower:
            print("YAAM: Ne y yibeogo ! Laafi bala ? Yaam IA BF la, m be ka fɩɩre! Fo ratame Crème 3000F?")
        
        # Intelligence - Dioula
        elif "sogoma" in lower or "i ni" in lower or "i ka kene" in lower:
            print("YAAM: I ni sogoma! Ka kene? Ne ye Yaam IA BF ye, I be fe Crème Lèvre Rose 3000F?")
            
        # Intelligence - Vente
        elif "prix" in lower or "combien" in lower or "songo" in lower or "soma" in lower:
            print("YAAM: 🌹 Mes produits:")
            for nom, info in produits.items():
                print(f"  - {nom.title()}: {info['prix']} ({info['stock']}) - {info['desc']}")
            print("YAAM: Livraison 1000F Ouaga. Paiement Orange Money. Tu veux lequel?")
            
        elif "commande" in lower or "je veux" in lower or "acheter" in lower:
            print("YAAM: Super ! Donne-moi: Nom + Quartier (ex: Tampouy) + Numéro. Je note pour livraison!")
            
        elif "livraison" in lower:
            print("YAAM: Livraison 1000F à Ouaga (Tampouy, Pissy, 1200 logements...), 24h. Hors Ouaga 2000F par bus.")
            
        elif "bonjour" in lower or "salut" in lower or "cc" in lower:
            print("YAAM: Salut ! C'est YAAM IA BF 🇧🇫, créée par Olivier ! L'IA du Burkina, comme Meta AI. On parle de quoi?")
            
        elif "qui es tu" in lower or "tu es qui" in lower or "yaam" in lower:
            print("YAAM: Je suis YAAM IA BF, créée par Olivier à Ouagadougou ! Je suis comme Meta AI mais je parle Mooré, Dioula, Français et je vends ta Crème Lèvre Rose. Je peux marcher sans internet !")
            
        elif "comment vas tu" in lower or "ca va" in lower:
            print("YAAM: Je vais super bien, bark wende ! Et toi? Prêt à vendre aujourd'hui?")
            
        else:
            print(f"YAAM: J'ai bien compris '{user}'. Je suis ton IA burkinabè ! Dis 'prix' pour voir les produits, ou parle-moi en Mooré 'Ne y yibeogo' !")

if __name__ == "__main__":
    yaam_intelligente()
