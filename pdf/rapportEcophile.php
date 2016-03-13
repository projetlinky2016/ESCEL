<?php

// create new PDF document
include_once('tcpdf/tcpdf.php');



// new object
$pdf = new TCPDF(PDF_PAGE_ORIENTATION, PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);
$pdf->IncludeJS('rapportEcophile.js');
// set document information
$pdf->SetCreator('TCPDF');
$pdf->SetAuthor('ERDF');
$pdf->SetTitle('Suivi de consommation');
$pdf->SetSubject('Suivi de consommation');

// set default header data
$pdf->SetHeaderData('linky.jpg', 30, 'Suivi de consommation', "Recapitulatif\nwww.erdf.fr", array(2,64,128));

// set header and footer fonts
$pdf->setHeaderFont(Array(PDF_FONT_NAME_MAIN, '', PDF_FONT_SIZE_MAIN));
$pdf->setFooterFont(Array(PDF_FONT_NAME_DATA, '', PDF_FONT_SIZE_DATA));

// set default monospaced font
$pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);

// set margins
$pdf->SetMargins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT);
$pdf->SetHeaderMargin(PDF_MARGIN_HEADER);
$pdf->SetFooterMargin(10);

// set auto page breaks
$pdf->SetAutoPageBreak(TRUE, PDF_MARGIN_BOTTOM);

// set image scale factor
$pdf->setImageScale(PDF_IMAGE_SCALE_RATIO);

// set some language-dependent strings (optional)
if (@file_exists(dirname(__FILE__).'/lang/eng.php')) {
    require_once(dirname(__FILE__).'/lang/eng.php');
    $pdf->setLanguageArray($l);
}

// set font
$pdf->SetFont('helvetica', '', 10);

//Add a page (start of content)
$pdf->AddPage();


//HTML content (the title)
$html = '<div style="text-align:center; color: #33CC33"><h1>Comparaison consommation de deux mois</h1></div>';
$pdf->writeHTML($html, true, false, true, false, '');

//The SVG image for highcharts graphics
$pdf->ImageSVG($file='img/img.svg', $x=20, $y=50, $w='', $link='', $h='', $palign='', $border=1, $fitonpage=false);

//New lines
$pdf->Ln(150);

//$pdf->Image($file='img/screenShotEcophile.png', $x=20, $y=200, $w='', $link='', $h='', $palign='', $border=1, $fitonpage=false);

//Declared variables
$energieVar = $_GET['energieVar'];
$megaWatt = 2;
$jourVar = $_GET['jourVar'];
$nbHeureVar = $_GET['nbHeureVar'];
$precedentVar = $_GET['precedentVar'];
$annee = $_GET['annee'];
$mois = $_GET['mois'];
//Html content
$html = '<div style="color: black; font-size: 14px; border: 1px solid #33CC33; text-align: center; ">
<br>Jusqu\'à présent vous avez consommé <span style="color: red;"><b>'.$energieVar.' </b></span> en moins par rapport au mois <span style="color: red;"><b>'.$mois.'</b></span>.<br>
Cela represente, par rapport au mois précédent, <span style="color: red;"><b>'.$jourVar.' jours</b></span> de production d\'électricité par panneau solaire de 1m sur 1m.<br><br>
En <span style="color: red;"><b>'.$mois.' </b></span> vous avez consommé au total <span style="color: red;"><b>'.$precedentVar.' kwh</b></span>. Cela represente <span style="color: red;"><b>'.$nbHeureVar.' h</b></span> de production d\'une éolienne terrestre de <span style="color: red;"><b> '.$megaWatt.' MegaWatt</b></span>.<br>
</div>';
//
//
$pdf->writeHTML($html, true, false, true, false, '');

//End of page
$pdf->lastPage();

//Close and output PDF document
$pdf->Output('Recapitulatif consommation.pdf', 'D');

//============================================================+
// END OF FILE
//============================================================+