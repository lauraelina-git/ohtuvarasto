from varasto import Varasto


def tarkista_varasto(varasto, nimi, lisays, otto, tulosta=True, debug=True):  # liikaa argumentteja
    if tulosta:
        print(f"{nimi} ennen muutoksia: {varasto}")
        if debug:
            if lisays > 0:
                varasto.lisaa_varastoon(lisays)
                print(f"Lisättiin {lisays}")
                if otto > 0:
                    varasto.ota_varastosta(otto)
                    print(f"Otetaan {otto}")
                    if varasto.saldo > 100:
                        print("Varasto yli täynnä!")  # 3 sisäkkäistä lohkoa
    print(f"{nimi} jälkeen: {varasto}")

def main():
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)

    tarkista_varasto(mehua, "Mehuvarasto", 50.7, 3.14)

    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehua}")
    print(f"Olutvarasto: {olutta}")

    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")

    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")

    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)

    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)

    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")

    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.otaVarastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")


if __name__ == "__main__":
    main()
