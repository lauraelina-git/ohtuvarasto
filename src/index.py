from varasto import Varasto


def tulosta_alustustilanne(mehua, olutta):
    """Tulostaa varastojen alkuperäisen tilanteen."""
    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehua}")
    print(f"Olutvarasto: {olutta}")


def testaa_olut_getterit(olutta):
    """Tulostaa olutvaraston getterien tulokset."""
    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")


def testaa_mehu_setterit(mehua):
    """Testaa mehuvaraston lisäystä ja ottoa."""
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")


def testaa_varaston_negatiivinen_tilavuus():
    """Testaa negatiivisen tilavuuden käsittelyä."""
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)


def testaa_varaston_negatiivinen_saldo():
    """Testaa negatiivisen aloitussaldon käsittelyä."""
    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)


def testaa_liian_suuri_lisays(olutta):
    """Testaa liian suuren lisäyksen käsittelyä."""
    print("Liian suuri lisäys:")
    print(f"Olutvarasto: {olutta}")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")


def testaa_negatiivinen_lisays(mehua):
    """Testaa negatiivisen lisäyksen käsittelyä."""
    print("Negatiivinen lisäys:")
    print(f"Mehuvarasto: {mehua}")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")


def testaa_liian_suuri_otto(olutta):
    """Testaa liian suuren oton käsittelyä."""
    print("Liian suuri otto:")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olutta}")


def testaa_negatiivinen_otto(mehua):
    """Testaa negatiivisen oton käsittelyä."""
    print("Negatiivinen otto:")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")


def aja_kaikki_testit(mehua, olutta):
    """Ajaa perustoiminnallisuudet."""
    tulosta_alustustilanne(mehua, olutta)
    testaa_olut_getterit(olutta)
    testaa_mehu_setterit(mehua)


def aja_virhetestit(mehua, olutta):
    """Ajaa virhetilanteet."""
    testaa_varaston_negatiivinen_tilavuus()
    testaa_varaston_negatiivinen_saldo()
    testaa_liian_suuri_lisays(olutta)
    testaa_negatiivinen_lisays(mehua)
    testaa_liian_suuri_otto(olutta)
    testaa_negatiivinen_otto(mehua)


def main():
    """Pääfunktio."""
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)
    aja_kaikki_testit(mehua, olutta)
    aja_virhetestit(mehua, olutta)

if __name__ == "__main__":
    main()
