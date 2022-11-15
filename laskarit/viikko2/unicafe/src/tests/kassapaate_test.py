import unittest

from kassapaate import *
from maksukortti import Maksukortti as kortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0

    def test_tilanteet_alussa(self):
        #alku-tilanteen tarkastus
        self.assertEqual(str(self.kassassa_rahaa), '100000')
        self.assertEqual(str(self.edulliset), '0')
        self.assertEqual(str(self.maukkaat), '0')
   
    def test_käteisosto_edulliset_yli(self):
        #maksaa enemmän kuin edullisen lounaan hintaa
        vastaus = Kassapaate.syo_edullisesti_kateisella(self, 250)
        edulliset = self.edulliset
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(vastaus), '10')
        self.assertEqual(str(edulliset), '1')
        self.assertEqual(str(kassa), '100240')
    
    def test_käteisosto_edulliset_riitävä(self):
        #maksaa saman verran kuin edullisen lounaan hintaa
        vastaus = Kassapaate.syo_edullisesti_kateisella(self, 240)
        edulliset = self.edulliset
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(vastaus), '0')
        self.assertEqual(str(edulliset), '1')
        self.assertEqual(str(kassa), '100240')

    def test_käteisosto_edulliset_ei_riitävä(self):
        #maksaa vähemmän kuin edullisen lounaan hintaa
        vastaus = Kassapaate.syo_edullisesti_kateisella(self, 230)
        edulliset = self.edulliset
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(vastaus), '230')
        self.assertEqual(str(edulliset), '0')
        self.assertEqual(str(kassa), '100000')

    def test_korttiosto_edulliset_riitävä(self):
        #kortilla on tarpeeksi rahaa, veloitetaan summa kortilta ja palautetaan True
        #kortilla on tarpeeksi rahaa, myytyjen lounaiden määrä kasvaa
        #kassassa oleva rahamäärä ei muutu kortilla ostettaessa
        vastaus = Kassapaate.syo_edullisesti_kortilla(self, kortti(1000))
        edulliset = self.edulliset
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(vastaus), 'True')
        self.assertEqual(str(edulliset), '1')
        self.assertEqual(str(kassa), '100000')
    
    def test_korttiosto_edulliset_ei_riitävä(self):
        #kortilla ei ole tarpeeksi rahaa, kortin rahamäärä ei muutu
        #myytyjen lounaiden määrä muuttumaton ja palautetaan False
        #kassassa oleva rahamäärä ei muutu kortilla ostettaessa
        vastaus = Kassapaate.syo_edullisesti_kortilla(self, kortti(230))
        edulliset = self.edulliset
        saldo = kortti(230)
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(saldo), 'Kortilla on rahaa 2.30 euroa')
        self.assertEqual(str(vastaus), 'False')
        self.assertEqual(str(edulliset), '0')
        self.assertEqual(str(kassa), '100000')

    def test_korttiosto_maukkaat_riitävä(self):
        #kortilla on tarpeeksi rahaa, veloitetaan summa kortilta ja palautetaan True
        #kortilla on tarpeeksi rahaa, myytyjen lounaiden määrä kasvaa
        #kassassa oleva rahamäärä ei muutu kortilla ostettaessa
        vastaus = Kassapaate.syo_maukkaasti_kortilla(self, kortti(1000))
        maukkaat = self.maukkaat
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(vastaus), 'True')
        self.assertEqual(str(maukkaat), '1')
        self.assertEqual(str(kassa), '100000')
    
    def test_korttiosto_edulliset_ei_riitävä(self):
        #kortilla ei ole tarpeeksi rahaa, kortin rahamäärä ei muutu
        #myytyjen lounaiden määrä muuttumaton ja palautetaan False
        #kassassa oleva rahamäärä ei muutu kortilla ostettaessa
        vastaus = Kassapaate.syo_maukkaasti_kortilla(self, kortti(300))
        maukkaat = self.maukkaat
        saldo = kortti(300)
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(saldo), 'Kortilla on rahaa 3.00 euroa')
        self.assertEqual(str(vastaus), 'False')
        self.assertEqual(str(maukkaat), '0')
        self.assertEqual(str(kassa), '100000')
    
    def test_kortille_lataaminen(self):
        #kortille rahaa ladattaessa kortin saldo muuttuu
        #kassassa oleva rahamäärä kasvaa ladatulla summalla
        Kassapaate.lataa_rahaa_kortille(self, kortti(0), 400)
        saldo = kortti(400)
        kassa = self.kassassa_rahaa
        
        self.assertEqual(str(saldo), 'Kortilla on rahaa 4.00 euroa')
        self.assertEqual(str(kassa), '100400')