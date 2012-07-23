'''
Created on Aug 21, 2012

@author: pete
'''
from bibfigure_captionextractor import CaptionExtractor
import unittest
from invenio.testutils import make_test_suite, run_test_suite
# test data
boxes = {
0 : {
(784, 1097, 176, 17) : """inally, the descriptor""",
(326, 554, 434, 16) : """
schemes with respect to repeatability, distinctiveness, a""",
(787, 1288, 172, 17) : """d complexity, while""",
(270, 1240, 527, 17) : """
comparison to the state-of-the-art are faster to compute, w""",
(787, 977, 172, 14) : """ons. The most valu-""",
(270, 1288, 516, 18) : """
requirements, like reducing the descriptor's dimension an""",
(269, 953, 515, 17) : """
vided into three main steps. First, 'interest points' are se""",
(782, 663, 121, 12) : """ methods to the""",
(588, 371, 6, 17) : """}""",
(326, 597, 484, 16) : """
This is achieved by relying on integral images for image conv""",
(559, 347, 4, 7) : """
1""",
(270, 1311, 284, 18) : """
keeping it sufficiently distinctive.""",
(656, 304, 6, 9) : """2""",
(326, 729, 477, 15) : """
evaluation set, as well as on imagery obtained in the context""",
(878, 490, 24, 11) : """ant""",
(839, 862, 121, 9) : """ same scene or""",
(326, 488, 84, 13) : """
Abstract.""",
(681, 417, 157, 11) : """@esat.kuleuven.be""",
(474, 373, 111, 15) : """bay, vangool""",
(804, 929, 155, 14) : """ work - can be di-""",
(783, 619, 120, 16) : """ and descriptors""",
(813, 750, 82, 13) : """rformance.""",
(270, 1264, 524, 17) : """
performance. In order to succeed, one has to strike a balance""",
(270, 1025, 514, 17) : """
reliably finds the same interest points under different viewi""",
(270, 857, 559, 18) : """
The task of finding correspondences between two images of the""",
(575, 350, 97, 12) : """ ETH Zurich""",
(665, 307, 171, 16) : """, and Luc Van Gool""",
(495, 307, 159, 17) : """, Tinne Tuytelaars""",
(872, 1216, 88, 17) : """, which in""",
(271, 1073, 85, 17) : """
descriptor""",
(832, 1168, 127, 17) : """is takes, and a""",
(357, 231, 516, 25) : """SURF: Speeded Up Robust Features""",
(596, 373, 168, 11) : """@vision.ee.ethz.ch""",
(269, 1096, 513, 18) : """
tion errors, and geometric and photometric deformations. F""",
(810, 728, 93, 13) : """ of a real-life""",
(270, 1192, 433, 14) : """
lower number of dimensions is therefore desirable.""",
(300, 1216, 569, 18) : """
It has been our goal to develop both a detector and descriptor""",
(364, 1073, 554, 16) : """ has to be distinctive and, at the same time, robust to noise, d""",
(787, 685, 116, 15) : """escription, and""",
(447, 1120, 512, 18) : """ between di\ufb00erent images. The matching is often based on a""",
(786, 953, 173, 14) : """lected at distinctive""",
(392, 641, 495, 16) : """, using a Hessian matrix-based measure for the detector, and""",
(828, 881, 131, 17) : """ calibration, 3D""",
(795, 532, 108, 16) : """usly proposed""",
(269, 1048, 503, 18) : """
the neighbourhood of every interest point is represented by""",
(326, 662, 448, 17) : """
distribution-based descriptor); and by simplifying these""",
(811, 597, 92, 16) : """olutions; by""",
(583, 1001, 67, 14) : """ detector""",
(759, 905, 200, 18) : """on are just a few. The""",
(672, 415, 6, 17) : """}""",
(327, 640, 4, 17) : """
(""",
(795, 1144, 164, 14) : """dean distance. The""",
(423, 488, 453, 16) : """ In this paper, we present a novel scale- and rotation-invari""",
(838, 304, 14, 9) : """12""",
(334, 642, 56, 12) : """in casu""",
(761, 554, 141, 16) : """nd robustness, yet""",
(270, 1144, 523, 18) : """
distance between the vectors, e.g. the Mahanalobis or Eucli""",
(326, 576, 360, 15) : """
can be computed and compared much faster.""",
(466, 371, 6, 17) : """
{""",
(270, 1168, 561, 17) : """
dimension of the descriptor has a direct impact on the time th""",
(486, 304, 5, 9) : """1""",
(778, 1048, 181, 15) : """ a feature vector. This""",
(801, 1264, 159, 14) : """ between the above""",
(399, 417, 270, 15) : """Tinne.Tuytelaars, Luc.Vangool""",
(270, 881, 548, 18) : """
object is part of many computer vision applications. Camera""",
(482, 391, 5, 7) : """
2""",
(920, 1074, 39, 12) : """etec-""",
(271, 810, 186, 17) : """
1 Introduction""",
(818, 707, 85, 12) : """ a standard""",
(326, 531, 468, 17) : """
bust Features). It approximates or even outperforms previo""",
(895, 645, 8, 8) : """ a""",
(326, 685, 460, 15) : """
essential. This leads to a combination of novel detection, d""",
(376, 307, 107, 17) : """
Herbert Bay""",
(785, 1025, 174, 18) : """ng conditions. Next,""",
(326, 619, 451, 15) : """
building on the strengths of the leading existing detectors""",
(659, 1001, 300, 17) : """ is its repeatability, i.e. whether it""",
(270, 905, 488, 18) : """
reconstruction, image registration, and object recogniti""",
(326, 707, 484, 15) : """
matching steps. The paper presents experimental results on""",
(818, 510, 84, 16) : """ed Up Ro-""",
(270, 1001, 301, 17) : """
able property of an interest point""",
(270, 929, 525, 18) : """
search for discrete image correspondences \u2013 the goal of this""",
(326, 750, 485, 16) : """
object recognition application. Both show SURF's strong pe""",
(269, 1122, 93, 12) : """
vectors are""",
(270, 977, 516, 18) : """
locations in the image, such as corners, blobs, and T-juncti""",
(371, 1120, 70, 14) : """ matched""",
(798, 1240, 162, 18) : """hile not sacri\ufb01cing""",
(326, 509, 491, 17) : """
interest point detector and descriptor, coined SURF (Speed""",
(390, 415, 6, 17) : """
{""",
(499, 394, 249, 12) : """ Katholieke Universiteit Leuven""",
},
1 : {
(270, 525, 555, 18) : """
ant detectors and descriptors. These seem to o\ufb00er a good comp""",
(270, 357, 537, 18) : """
on benchmark image sets as well as on a real object recognitio""",
(790, 381, 169, 14) : """lso more distinctive""",
(270, 715, 539, 19) : """
scriptor, which we refer to as 'upright SURF' (U-SURF). Inde""",
(270, 740, 494, 18) : """
applications, like mobile robot navigation or visual touri""",
(797, 501, 162, 18) : """age rotation invari-""",
(827, 525, 133, 14) : """romise between""",
(300, 884, 503, 18) : """
The paper is organised as follows. Section 2 describes relat""",
(802, 1143, 157, 19) : """ [1]. This allows to""",
(270, 1215, 526, 19) : """
Laplacian (which corresponds to the trace of the Hessian mat""",
(270, 1264, 493, 18) : """
and scale-invariant feature detectors with high repeatabi""",
(773, 692, 186, 17) : """nly version of our de-""",
(864, 429, 95, 14) : """e settled is""",
(270, 284, 506, 19) : """
ing datasets have been performed [7\u20139]. While constructing""",
(270, 1192, 550, 17) : """
experimented with both the determinant of the Hessian matri""",
(495, 1073, 464, 17) : """ The most widely used detector probably is the Har-""",
(806, 549, 153, 17) : """formations. Skew,""",
(270, 572, 514, 18) : """
anisotropic scaling, and perspective e\ufb00ects are assumed to""",
(811, 716, 149, 17) : """ed, in quite a few""",
(796, 333, 163, 17) : """ In our experiments""",
(782, 285, 177, 14) : """ our fast detector and""",
(270, 788, 510, 17) : """
rotation invariance in such cases is not only increased spee""",
(270, 1073, 211, 14) : """
Interest Point Detectors""",
(781, 453, 178, 18) : """he expected geomet-""",
(784, 620, 175, 15) : """l a\ufb03ne-invariant fea-""",
(270, 835, 530, 18) : """
simple linear model with a scale factor and o\ufb00set. Notice tha""",
(270, 764, 521, 17) : """
often only rotates about the vertical axis. The bene\ufb01t of avo""",
(749, 261, 210, 14) : """aluations on benchmark-""",
(270, 668, 537, 18) : """
really large viewpoint changes are to be expected. In some ca""",
(299, 429, 563, 18) : """
When working with local features, a \ufb01rst issue that needs to b""",
(270, 1240, 540, 17) : """
like structures. Mikolajczyk and Schmid re\ufb01ned this method""",
(270, 860, 236, 17) : """
descriptor don't use colour.""",
(270, 908, 506, 17) : """
our results are founded. Section 3 describes the interest po""",
(793, 812, 166, 17) : """tions, we assume a""",
(270, 381, 518, 18) : """
resulting detector and descriptor are not only faster, but a""",
(270, 1120, 547, 17) : """
second-moment matrix. However, Harris corners are not scal""",
(793, 572, 166, 15) : """ be second-order ef-""",
(798, 1215, 161, 19) : """rix) to detect blob-""",
(778, 908, 181, 14) : """int detection scheme.""",
(765, 740, 195, 18) : """st guiding, the camera""",
(765, 1264, 194, 17) : """lity, which they coined""",
(270, 1095, 528, 19) : """
ris corner detector [10], proposed back in 1988, based on the""",
(269, 453, 510, 17) : """
the required level of invariance. Clearly, this depends on t""",
(270, 187, 387, 16) : """2 H. Bay, T. Tuytelaars, and L. Van Gool""",
(270, 596, 514, 18) : """
fects, that are covered to some degree by the overall robustn""",
(795, 477, 164, 17) : """ned by the possible""",
(809, 669, 152, 16) : """ses, even rotation""",
(805, 1287, 155, 19) : """e-adapted) Harris""",
(807, 1096, 152, 18) : """ eigenvalues of the""",
(801, 1312, 158, 16) : """e location, and the""",
(270, 1019, 202, 17) : """
2 Related Work""",
(821, 1192, 138, 14) : """x as well as the""",
(270, 333, 518, 18) : """
a feel for what are the aspects contributing to performance.""",
(270, 501, 525, 18) : """
changes in viewing conditions. Here, we focus on scale and im""",
(270, 932, 495, 17) : """
In section 4, the new descriptor is presented. Finally, sect""",
(813, 1240, 147, 18) : """, creating robust""",
(769, 309, 190, 18) : """us work in order to get""",
(269, 644, 523, 18) : """
tures often has a negative impact on their robustness and doe""",
(270, 1144, 521, 18) : """
deberg introduced the concept of automatic scale selection""",
(270, 1311, 530, 15) : """
measure or the determinant of the Hessian matrix to select th""",
(805, 884, 155, 17) : """ed work, on which""",
(270, 549, 534, 18) : """
feature complexity and robustness to commonly occurring de""",
(785, 596, 174, 18) : """ess of the descriptor.""",
(270, 477, 523, 17) : """
ric and photometric deformations, which in turn are determi""",
(270, 405, 201, 17) : """
and equally repeatable.""",
(801, 836, 158, 14) : """t our detector and""",
(270, 620, 512, 19) : """
As also claimed by Lowe [2], the additional complexity of ful""",
(808, 1168, 151, 14) : """cteristic scale. He""",
(270, 309, 497, 18) : """
descriptor, we built on the insights gained from this previo""",
(782, 788, 178, 17) : """d, but also increased""",
(767, 932, 192, 17) : """ion 5 shows the exper-""",
(793, 764, 168, 18) : """iding the overkill of""",
(809, 357, 150, 17) : """n application, the""",
(300, 237, 511, 18) : """
A wide variety of detectors and descriptors have already bee""",
(270, 260, 478, 19) : """
literature (e.g. [1\u20136]). Also, detailed comparisons and ev""",
(270, 956, 433, 17) : """
imental results and section 6 concludes the paper.""",
(270, 1168, 536, 18) : """
detect interest points in an image, each with their own chara""",
(794, 644, 165, 18) : """s not pay o\ufb00, unless""",
(270, 692, 501, 18) : """
invariance can be left out, resulting in a scale-invariant o""",
(270, 812, 522, 18) : """
discriminative power. Concerning the photometric deforma""",
(813, 237, 146, 17) : """n proposed in the""",
(270, 1287, 534, 19) : """
Harris-Laplace and Hessian-Laplace [11]. They used a (scal""",
(818, 1121, 141, 13) : """e-invariant. Lin-""",
},
2 : {
(801, 953, 158, 19) : """he same paper [8],""",
(269, 1074, 547, 17) : """
tical uses, and hence also the most widely used nowadays. It i""",
(270, 906, 512, 18) : """
dimensional descriptor which is fast for matching, but prov""",
(269, 881, 579, 19) : """
thankar [4] applied PCA on the gradient image. This PCA-SIFT""",
(270, 236, 544, 19) : """
Laplacian to select the scale. Focusing on speed, Lowe [12] a""",
(793, 763, 167, 17) : """ors. The descriptor""",
(792, 333, 167, 18) : """ region detector pro-""",
(270, 357, 123, 17) : """
posed by Jurie""",
(818, 1312, 141, 14) : """ased on the Hes-""",
(817, 1074, 104, 14) : """s distinctive""",
(299, 858, 543, 17) : """
Various re\ufb01nements on this basic scheme have been proposed.""",
(858, 882, 101, 18) : """ yields a 36-""",
(814, 787, 146, 17) : """riented gradients""",
(847, 929, 113, 19) : """ [8] and slower""",
(821, 1002, 138, 17) : """wever, GLOH is""",
(270, 499, 524, 19) : """
matrix rather than its trace (the Laplacian) seems advantag""",
(270, 333, 516, 18) : """
maximises the entropy within the region, and the edge-based""",
(782, 405, 160, 17) : """cope of this paper.""",
(755, 618, 212, 19) : """17], complex features [18,""",
(269, 452, 545, 19) : """
we can conclude that (1) Hessian-based detectors are more st""",
(832, 1049, 127, 18) : """riptor for prac-""",
(848, 428, 111, 19) : """risons [15,8],""",
(451, 356, 508, 19) : """ [14]. They seem less amenable to acceleration though. Also,""",
(931, 1074, 31, 14) : """ and""",
(820, 691, 140, 17) : """n to outperform""",
(772, 476, 189, 15) : """minant of the Hessian""",
(752, 667, 207, 18) : """ the interest point neigh-""",
(829, 1169, 131, 17) : """ne applications""",
(601, 187, 358, 15) : """SURF: Speeded Up Robust Features 3""",
(270, 1120, 582, 19) : """
implemented SIFT on a Field Programmable Gate Array (FPGA) a""",
(270, 1097, 478, 18) : """
relatively fast, which is crucial for on-line applications""",
(270, 785, 542, 19) : """
in [2], called SIFT for short, computes a histogram of local o""",
(802, 1246, 12, 12) : """y.""",
(851, 858, 108, 14) : """ Ke and Suk-""",
(270, 667, 475, 18) : """
senting the distribution of smaller-scale features within""",
(879, 1097, 41, 14) : """ et al.""",
(270, 405, 510, 18) : """
longer viewpoint changes. However, these fall outside the s""",
(772, 285, 187, 17) : """ve been proposed. Ex-""",
(270, 477, 501, 17) : """
able than their Harris-based counterparts. Using the deter""",
(809, 715, 151, 14) : """ture a substantial""",
(270, 1241, 530, 18) : """
speed up the matching step, but this results in lower accurac""",
(826, 978, 133, 17) : """ch proved to be""",
(750, 1097, 118, 18) : """. Recently, Se""",
(402, 357, 39, 14) : """ et al.""",
(740, 524, 220, 14) : """mations like the DoG can""",
(816, 237, 143, 17) : """pproximated the""",
(271, 642, 477, 19) : """
19], steerable \ufb01lters [20], phase-based local features [21""",
(562, 838, 9, 9) : """ """,
(270, 595, 169, 17) : """
Feature Descriptors""",
(830, 809, 129, 19) : """ional vector (8""",
(808, 308, 152, 19) : """ Brady [13], which""",
(404, 1288, 541, 17) : """ In this paper, we propose a novel detector-descriptor schem""",
(272, 1288, 118, 17) : """
Our approach""",
(270, 954, 529, 18) : """
feature computation reduces the e\ufb00ect of fast matching. In t""",
(932, 1096, 26, 19) : """ [22]""",
(450, 595, 510, 18) : """ An even larger variety of feature descriptors has been pro-""",
(800, 930, 38, 14) : """ et al.""",
(300, 285, 471, 17) : """
Several other scale-invariant interest point detectors ha""",
(777, 1216, 182, 19) : """native [2] in order to""",
(810, 1192, 148, 19) : """iption, matching)""",
(269, 714, 538, 19) : """
the others [7]. This can be explained by the fact that they cap""",
(270, 739, 519, 17) : """
amount of information about the spatial intensity patterns""",
(817, 453, 142, 17) : """able and repeat-""",
(269, 930, 524, 18) : """
tive than SIFT in a second comparative study by Mikolajczyk""",
(947, 1293, 12, 12) : """e,""",
(813, 1145, 146, 18) : """onality of the de-""",
(269, 978, 556, 17) : """
the authors have proposed a variant of SIFT, called GLOH, whi""",
(300, 1049, 530, 18) : """
The SIFT descriptor still seems to be the most appealing desc""",
(270, 1169, 558, 18) : """
scriptor is a drawback of SIFT at the matching step. For on-li""",
(270, 309, 530, 18) : """
amples are the salient region detector proposed by Kadir and""",
(795, 500, 164, 17) : """eous, as it \ufb01res less""",
(270, 548, 441, 18) : """
bring speed at a low cost in terms of lost accuracy.""",
(270, 1311, 546, 19) : """
coined SURF (Speeded-Up Robust Features). The detector is b""",
(580, 833, 139, 19) : """ 4 location bins).""",
(270, 834, 283, 14) : """
orientation bins for each of the 4""",
(269, 763, 522, 18) : """
time being robust to small deformations or localisation err""",
(270, 1026, 284, 17) : """
computationally more expensive.""",
(270, 523, 469, 19) : """
on elongated, ill-localised structures. Also, (2) approxi""",
(832, 260, 58, 19) : """) \ufb01lter.""",
(792, 739, 168, 16) : """, while at the same""",
(270, 811, 558, 17) : """
around the interest point and stores the bins in a 128-dimens""",
(773, 381, 187, 17) : """ed that can cope with""",
(270, 381, 501, 17) : """
several a\ufb03ne-invariant feature detectors have been propos""",
(300, 428, 546, 18) : """
By studying the existing detectors and from published compa""",
(270, 1145, 541, 18) : """
its speed by an order of magnitude. However, the high dimensi""",
(270, 260, 559, 19) : """
Laplacian of Gaussian (LoG) by a Di\ufb00erence of Gaussians (DoG""",
(270, 1217, 506, 17) : """
should be faster still. Lowe proposed a best-bin-\ufb01rst alter""",
(270, 1192, 538, 19) : """
on a regular PC, each one of the three steps (detection, descr""",
(270, 1002, 549, 14) : """
even more distinctive with the same number of dimensions. Ho""",
(270, 690, 549, 19) : """
bourhood. The latter, introduced by Lowe [2], have been show""",
(784, 906, 175, 14) : """ed to be less distinc-""",
(270, 618, 482, 19) : """
posed, like Gaussian derivatives [16], moment invariants [""",
(854, 1121, 106, 17) : """nd improved""",
(751, 642, 208, 19) : """], and descriptors repre-""",
},
3 : {
(775, 611, 2, 2) : """.""",
(825, 561, 18, 9) : """=0""",
(270, 1071, 526, 19) : """
in the relevant 2D case [25]. Hence, the importance of the Gau""",
(741, 1322, 15, 8) : """yy""",
(669, 801, 15, 14) : """ H""",
(771, 545, 9, 12) : """\u2264""",
(792, 777, 167, 17) : """ both. Given a point""",
(868, 551, 26, 17) : """i, j""",
(270, 428, 544, 18) : """
not only the matching speed, but also the robustness of the de""",
(571, 934, 11, 8) : """ x""",
(789, 476, 171, 18) : """ fast implementation""",
(783, 549, 7, 6) : """x""",
(269, 529, 11, 8) : """
x""",
(474, 801, 9, 13) : """ I""",
(677, 878, 16, 8) : """yy""",
(272, 940, 16, 10) : """
\u2202x""",
(523, 855, 26, 19) : """) =""",
(911, 934, 11, 8) : """x""",
(696, 556, 11, 8) : """x""",
(486, 801, 176, 17) : """, the Hessian matrix""",
(331, 902, 12, 13) : """ L""",
(797, 550, 18, 19) : """
P""",
(797, 1073, 163, 13) : """ssian seems to have""",
(461, 856, 15, 14) : """
H""",
(731, 800, 30, 19) : """) in""",
(270, 236, 536, 19) : """
sian matrix [11,1], but uses a very basic approximation, jus""",
(697, 843, 4, 19) : """(""",
(374, 1264, 534, 18) : """9 box \ufb01lters in Fig. 1 are approximations for Gaussian second""",
(795, 1143, 163, 19) : """h box \ufb01lters (Fig. 1""",
(571, 868, 12, 13) : """
L""",
(816, 429, 70, 17) : """scriptor.""",
(797, 381, 162, 14) : """obustness. We also""",
(816, 561, 6, 12) : """
j""",
(351, 523, 448, 19) : """) represents the sum of all pixels in the input image""",
(886, 940, 16, 8) : """yy""",
(270, 551, 233, 18) : """
region formed by the point""",
(511, 556, 11, 8) : """ x""",
(408, 901, 552, 19) : """) is the convolution of the Gaussian second order derivative""",
(331, 928, 141, 19) : """) with the image""",
(801, 1216, 159, 18) : """ing the discretised""",
(481, 1300, 2, 2) : """.""",
(744, 929, 12, 13) : """ L""",
(270, 776, 514, 19) : """
detector [11]), we rely on the determinant of the Hessian for""",
(760, 1312, 41, 16) : """, and""",
(860, 806, 10, 8) : """ \u03c3""",
(604, 867, 4, 19) : """(""",
(300, 953, 511, 17) : """
Gaussians are optimal for scale-space analysis, as shown in""",
(604, 843, 4, 19) : """(""",
(269, 705, 554, 18) : """
We base our detector on the Hessian matrix because of its good""",
(270, 476, 512, 19) : """
cept of integral images, as de\ufb01ned by [23]. They allow for the""",
(798, 333, 162, 18) : """ integral images for""",
(771, 561, 18, 9) : """=0""",
(317, 806, 32, 12) : """x, y""",
(677, 1312, 15, 13) : """ D""",
(937, 855, 21, 19) : """ (1)""",
(925, 934, 21, 12) : """, \u03c3""",
(269, 261, 499, 18) : """
very basic Laplacian-based detector. It relies on integral""",
(570, 844, 12, 13) : """
L""",
(288, 523, 26, 19) : """ = (""",
(769, 806, 11, 8) : """ x""",
(270, 1144, 523, 17) : """
approximations, we push the approximation even further wit""",
(821, 952, 138, 19) : """ [24]. In practice,""",
(486, 861, 11, 8) : """x""",
(610, 873, 11, 8) : """x""",
(365, 901, 4, 19) : """(""",
(421, 1293, 10, 8) : """ \u03c3""",
(806, 1049, 154, 17) : """nown to not apply""",
(351, 800, 115, 19) : """) in an image""",
(270, 976, 528, 19) : """
however, the Gaussian needs to be discretised and cropped (F""",
(480, 855, 4, 19) : """(""",
(270, 309, 522, 17) : """
scriptor, on the other hand, describes a distribution of Haa""",
(703, 873, 11, 8) : """x""",
(270, 657, 298, 17) : """
3 Fast-Hessian Detector""",
(837, 549, 7, 8) : """y""",
(765, 868, 2, 5) : """
,""",
(270, 381, 525, 18) : """
putation and matching, and increasing simultaneously the r""",
(677, 854, 16, 8) : """xy""",
(497, 930, 66, 16) : """ in point""",
(825, 545, 9, 12) : """\u2264""",
(812, 453, 147, 17) : """y discuss the con-""",
(817, 405, 143, 17) : """, which increases""",
(690, 550, 4, 19) : """(""",
(807, 236, 152, 19) : """t as DoG [2] is a""",
(740, 843, 4, 19) : """)""",
(647, 843, 4, 19) : """)""",
(270, 1288, 140, 14) : """
derivatives with""",
(269, 902, 50, 14) : """
where""",
(270, 357, 517, 18) : """
speed. Moreover, only 64 dimensions are used, reducing the t""",
(300, 934, 9, 12) : """g""",
(480, 929, 9, 13) : """ I""",
(842, 499, 119, 19) : """) at a location""",
(697, 867, 4, 19) : """(""",
(270, 1001, 504, 18) : """
even with Gaussian \ufb01lters aliasing still occurs as soon as th""",
(675, 558, 11, 9) : """\u03a3""",
(807, 525, 9, 13) : """ I""",
(647, 867, 4, 19) : """)""",
(277, 925, 8, 10) : """
\u2202""",
(693, 1322, 16, 6) : """xx""",
(584, 929, 152, 17) : """, and similarly for""",
(809, 1312, 15, 13) : """ D""",
(300, 1264, 48, 14) : """
The 9""",
(584, 854, 16, 6) : """xx""",
(905, 928, 4, 19) : """(""",
(845, 1312, 115, 17) : """. The weights""",
(270, 1120, 527, 18) : """
As Gaussian \ufb01lters are non-ideal in any case, and given Lowe'""",
(666, 551, 9, 13) : """ I""",
(530, 551, 127, 18) : """ and the origin,""",
(298, 575, 497, 17) : """ calculated, it only takes four additions to calculate the su""",
(879, 801, 80, 14) : """ is de\ufb01ned""",
(713, 1323, 2, 5) : """,""",
(270, 599, 503, 18) : """
over any upright, rectangular area, independent of its size""",
(777, 928, 4, 19) : """(""",
(796, 575, 163, 14) : """m of the intensities""",
(270, 405, 545, 18) : """
present a new indexing step based on the sign of the Laplacian""",
(784, 934, 11, 8) : """x""",
(765, 546, 4, 9) : """i""",
(750, 841, 5, 47) : """
\uffff""",
(371, 907, 11, 8) : """x""",
(916, 1264, 44, 14) : """ order""",
(789, 1025, 170, 18) : """ppear while going to""",
(279, 582, 11, 9) : """\u03a3""",
(862, 550, 4, 19) : """(""",
(872, 929, 12, 13) : """ L""",
(286, 923, 4, 6) : """
2""",
(356, 1268, 9, 9) : """""",
(846, 753, 114, 17) : """ssian-Laplace""",
(812, 729, 148, 14) : """ di\ufb00erent measure""",
(897, 550, 63, 19) : """). With""",
(824, 524, 136, 18) : """ of a rectangular""",
(765, 561, 4, 9) : """
i""",
(319, 934, 10, 8) : """\u03c3""",
(694, 806, 11, 8) : """x""",
(270, 1097, 551, 17) : """
been somewhat overrated in this regard, and here we test a sim""",
(384, 907, 22, 12) : """, \u03c3""",
(291, 939, 4, 6) : """2""",
(270, 1024, 517, 18) : """
sub-sampled. Also, the property that no new structures can a""",
(688, 800, 4, 19) : """(""",
(785, 505, 7, 9) : """e""",
(797, 934, 21, 12) : """, \u03c3""",
(664, 844, 12, 13) : """ L""",
(744, 550, 18, 19) : """
P""",
(584, 878, 16, 8) : """xy""",
(288, 800, 26, 19) : """ = (""",
(829, 505, 11, 8) : """x""",
(561, 841, 5, 47) : """
\uffff""",
(789, 357, 170, 14) : """ime for feature com-""",
(799, 501, 9, 13) : """ I""",
(709, 550, 27, 19) : """) =""",
(269, 333, 519, 18) : """
within the interest point neighbourhood. Again, we exploit""",
(808, 508, 11, 9) : """\u03a3""",
(777, 261, 182, 18) : """ images to reduce the""",
(850, 551, 9, 13) : """ I""",
(948, 928, 11, 19) : """).""",
(270, 825, 81, 14) : """
as follows""",
(740, 867, 4, 19) : """)""",
(799, 1120, 160, 14) : """s success with LoG""",
(823, 499, 4, 19) : """(""",
(610, 849, 11, 8) : """x""",
(270, 1216, 529, 17) : """
results section, the performance is comparable to the one us""",
(499, 861, 21, 12) : """, \u03c3""",
(270, 1192, 497, 18) : """
evaluated very fast using integral images, independently o""",
(769, 1192, 190, 14) : """f size. As shown in the""",
(270, 500, 514, 18) : """
of box type convolution \ufb01lters. The entry of an integral imag""",
(269, 806, 11, 8) : """
x""",
(820, 928, 44, 19) : """) and""",
(270, 1049, 534, 17) : """
lower resolutions may have been proven in the 1D case, but is k""",
(703, 849, 11, 8) : """x""",
(312, 928, 4, 19) : """(""",
(270, 187, 387, 16) : """4 H. Bay, T. Tuytelaars, and L. Van Gool""",
(800, 1168, 159, 17) : """atives, and can be""",
(816, 546, 6, 12) : """j""",
(300, 452, 511, 18) : """
In order to make the paper more self-contained, we succinctl""",
(724, 1312, 15, 13) : """ D""",
(270, 729, 534, 18) : """
computation time and accuracy. However, rather than using a""",
(270, 285, 525, 17) : """
computation time and we therefore call it the 'Fast-Hessian""",
(716, 849, 22, 12) : """, \u03c3""",
(270, 752, 574, 19) : """
for selecting the location and the scale (as was done in the He""",
(316, 529, 33, 12) : """x, y""",
(623, 873, 22, 11) : """, \u03c3""",
(826, 1322, 16, 8) : """xy""",
(793, 309, 167, 17) : """r-wavelet responses""",
(823, 1097, 136, 17) : """pler alternative.""",
(270, 1167, 529, 19) : """
right half). These approximate second order Gaussian deriv""",
(707, 806, 22, 12) : """, \u03c3""",
(486, 1287, 474, 19) : """2 and represent our lowest scale (i.e. highest spatial""",
(758, 940, 16, 8) : """xy""",
(624, 849, 21, 12) : """, \u03c3""",
(270, 575, 9, 13) : """
I""",
(444, 1288, 33, 13) : """ = 1""",
(797, 285, 162, 14) : """' detector. The de-""",
(345, 913, 16, 6) : """xx""",
(270, 1240, 205, 17) : """
and cropped Gaussians.""",
(716, 873, 21, 11) : """, \u03c3""",
(270, 1311, 398, 19) : """
resolution). We denote our approximations by""",
(788, 801, 64, 14) : """ at scale""",
(664, 868, 12, 13) : """ L""",
(800, 976, 159, 19) : """ig. 1 left half), and""",
(775, 1001, 185, 18) : """e resulting images are""",
(831, 705, 129, 17) : """ performance in""",
},
4 : {
(269, 1097, 367, 17) : """
the interest points can be doubled as well.""",
(837, 388, 123, 16) : """d order partial""",
(270, 1001, 443, 17) : """
our \ufb01lters. Speci\ufb01cally, this results in \ufb01lters of size 9""",
(270, 977, 526, 18) : """
into account the discrete nature of integral images and the s""",
(608, 576, 11, 9) : """D""",
(937, 627, 21, 19) : """ (2)""",
(937, 1001, 23, 17) : """27,""",
(735, 1001, 38, 17) : """9, 15""",
(300, 714, 556, 18) : """
Scale spaces are usually implemented as image pyramids. The""",
(663, 580, 8, 6) : """F""",
(833, 786, 126, 17) : """he output of a""",
(605, 575, 1, 13) : """|""",
(270, 786, 561, 18) : """
images, we do not have to iteratively apply the same \ufb01lter to t""",
(270, 929, 39, 14) : """
scale""",
(270, 410, 106, 13) : """
derivatives in""",
(270, 809, 501, 18) : """
previously \ufb01ltered layer, but instead can apply such \ufb01lters""",
(270, 1168, 172, 17) : """
\ufb01lter corresponds to""",
(557, 627, 26, 19) : """) =""",
(686, 627, 15, 19) : """ (0""",
(798, 977, 163, 17) : """peci\ufb01c structure of""",
(866, 1001, 49, 17) : """21, 27""",
(270, 1048, 500, 18) : """
accordingly. Hence, for each new octave, the \ufb01lter size incr""",
(719, 1005, 9, 9) : """""",
(625, 1173, 7, 9) : """ s""",
(527, 576, 9, 9) : """L""",
(573, 575, 12, 13) : """2)""",
(270, 953, 535, 18) : """
layers are obtained by \ufb01ltering the image with gradually big""",
(335, 387, 500, 17) : """ Left to right: the (discretised and cropped) Gaussian secon""",
(756, 576, 14, 2) : """...""",
(780, 1005, 9, 9) : """x""",
(269, 834, 532, 17) : """
the same speed directly on the original image, and even in par""",
(735, 639, 16, 8) : """xy""",
(538, 583, 13, 4) : """xx""",
(592, 1240, 368, 18) : """ 3 neighbourhood is applied. The maxima""",
(468, 1169, 29, 13) : """ = 3""",
(527, 559, 9, 9) : """L""",
(639, 575, 16, 13) : """(9)""",
(270, 514, 533, 18) : """
applied to the rectangular regions are kept simple for compu""",
(608, 559, 11, 9) : """D""",
(725, 565, 28, 13) : """912""",
(538, 566, 13, 6) : """xy""",
(270, 666, 517, 17) : """
Furthermore, the \ufb01lter responses are normalised with respe""",
(789, 666, 170, 14) : """ct to the mask size.""",
(522, 1169, 6, 13) : """1""",
(591, 629, 15, 13) : """ D""",
(270, 905, 64, 14) : """
above 9""",
(270, 856, 488, 19) : """
latter is not exploited here). Therefore, the scale space is""",
(270, 1264, 551, 17) : """
of the determinant of the Hessian matrix are then interpolat""",
(569, 567, 1, 1) : """.""",
(490, 629, 15, 14) : """H""",
(300, 1120, 524, 18) : """
As the ratios of our \ufb01lter layout remain constant after scali""",
(659, 575, 1, 13) : """|""",
(341, 909, 9, 9) : """x""",
(270, 1144, 511, 18) : """
imated Gaussian derivatives scale accordingly. Thus, for e""",
(801, 738, 158, 17) : """ampled in order to""",
(635, 1168, 325, 17) : """. Furthermore, as the Frobenius norm""",
(782, 1144, 132, 17) : """xample, our 27""",
(803, 832, 156, 19) : """allel (although the""",
(767, 1287, 192, 19) : """ [27]. Scale space inter-""",
(450, 1174, 10, 8) : """ \u03c3""",
(508, 639, 46, 8) : """approx""",
(666, 637, 12, 1) : """ \u2212""",
(300, 1216, 563, 18) : """
In order to localise interest points in the image and over sca""",
(772, 1047, 188, 19) : """ease is doubled (going""",
(948, 565, 11, 13) : """ is""",
(942, 1145, 18, 13) : """ 27""",
(270, 538, 561, 18) : """
but we need to further balance the relative weights in the exp""",
(921, 1005, 9, 9) : """x""",
(569, 584, 1, 1) : """.""",
(393, 410, 112, 13) : """-direction and""",
(782, 1025, 178, 14) : """zes should also scale""",
(270, 432, 334, 16) : """
\ufb01lters. The grey regions are equal to zero.""",
(593, 580, 8, 6) : """F""",
(926, 572, 10, 9) : """F""",
(639, 558, 16, 13) : """(9)""",
(709, 629, 8, 13) : """9""",
(584, 1180, 2, 2) : """.""",
(875, 905, 85, 14) : """ill refer as""",
(659, 558, 1, 13) : """|""",
(573, 1244, 9, 9) : """ x""",
(270, 1240, 256, 17) : """
maximum suppression in a 3""",
(754, 627, 4, 19) : """)""",
(607, 639, 16, 6) : """xx""",
(589, 575, 1, 13) : """|""",
(270, 1192, 522, 17) : """
remains constant for our \ufb01lters, they are already scale norm""",
(775, 881, 184, 17) : """ze. The output of the""",
(533, 410, 427, 16) : """-direction, and our approximations thereof using box""",
(806, 953, 154, 18) : """ger masks, taking""",
(761, 625, 6, 9) : """2""",
(923, 1148, 9, 9) : """ x""",
(523, 558, 1, 13) : """
|""",
(555, 558, 11, 13) : """(1""",
(536, 1244, 9, 9) : """ x""",
(922, 563, 1, 19) : """|""",
(823, 1264, 136, 14) : """ed in scale and""",
(763, 934, 10, 8) : """ \u03c3""",
(793, 1072, 168, 14) : """or the extraction of""",
(269, 591, 277, 17) : """
the Frobenius norm. This yields""",
(820, 565, 73, 16) : """9, where""",
(621, 566, 13, 4) : """xx""",
(626, 629, 15, 13) : """D""",
(826, 1120, 134, 18) : """ng, the approx-""",
(812, 941, 2, 2) : """.""",
(805, 565, 8, 13) : """ 0""",
(555, 575, 11, 13) : """(1""",
(779, 809, 181, 18) : """ of any size at exactly""",
(715, 1288, 40, 14) : """ et al.""",
(601, 187, 358, 15) : """SURF: Speeded Up Robust Features 5""",
(825, 762, 135, 18) : """ers and integral""",
(593, 563, 8, 6) : """F""",
(792, 1312, 168, 14) : """ce in scale between""",
(367, 928, 390, 19) : """2 (corresponding to Gaussian derivatives with""",
(793, 1191, 90, 19) : """alised [26].""",
(721, 576, 2, 2) : """.""",
(513, 415, 18, 11) : """ xy""",
(851, 1005, 9, 9) : """x""",
(771, 640, 2, 2) : """.""",
(523, 575, 1, 13) : """
|""",
(781, 569, 13, 8) : """ \u2243""",
(803, 514, 156, 18) : """tational e\ufb03ciency,""",
(555, 1240, 8, 13) : """ 3""",
(384, 415, 8, 11) : """ y""",
(270, 1071, 523, 19) : """
from 6 to 12 to 24). Simultaneously, the sampling intervals f""",
(817, 928, 143, 19) : """2). The following""",
(270, 388, 53, 16) : """
Fig.1.""",
(270, 690, 530, 18) : """
This guarantees a constant Frobenius norm for any \ufb01lter size""",
(269, 881, 505, 18) : """
the \ufb01lter size rather than iteratively reducing the image si""",
(816, 576, 2, 2) : """.""",
(909, 570, 9, 9) : """x""",
(316, 934, 7, 9) : """ s""",
(781, 930, 27, 13) : """ = 1""",
(797, 1001, 46, 17) : """15, 21""",
(270, 1024, 511, 19) : """
etc. At larger scales, the step between consecutive \ufb01lter si""",
(704, 640, 2, 2) : """.""",
(766, 857, 194, 18) : """ analysed by up-scaling""",
(537, 1169, 44, 13) : """2 = 3""",
(643, 639, 15, 8) : """yy""",
(604, 558, 1, 13) : """|""",
(363, 941, 2, 2) : """.""",
(905, 563, 1, 19) : """ |""",
(867, 715, 93, 17) : """ images are""",
(455, 627, 33, 19) : """
det(""",
(270, 738, 529, 17) : """
repeatedly smoothed with a Gaussian and subsequently sub-s""",
(358, 905, 516, 18) : """9 \ufb01lter is considered as the initial scale layer, to which we w""",
(270, 1311, 521, 18) : """
polation is especially important in our case, as the di\ufb00eren""",
(833, 538, 126, 14) : """ression for the""",
(865, 1216, 94, 17) : """les, a non-""",
(663, 563, 8, 6) : """F""",
(270, 565, 240, 14) : """
Hessian's determinant with""",
(719, 629, 15, 13) : """D""",
(803, 702, 2, 2) : """.""",
(589, 1169, 28, 13) : """6 =""",
(504, 1172, 9, 9) : """x""",
(686, 565, 32, 13) : """ = 0""",
(532, 1180, 2, 2) : """.""",
(589, 558, 1, 13) : """|""",
(331, 930, 28, 13) : """ = 1""",
(573, 558, 11, 13) : """2)""",
(270, 762, 553, 18) : """
achieve a higher level of the pyramid. Due to the use of box \ufb01lt""",
(270, 1288, 435, 18) : """
image space with the method proposed by Brown""",
(621, 583, 13, 6) : """xy""",
},
5 : {
(270, 857, 502, 18) : """
orientations of gradients reduces the e\ufb00ect of photometric""",
(269, 1024, 538, 18) : """
that is not invariant to image rotation and therefore faster""",
(835, 977, 124, 14) : """lained in turn.""",
(294, 1197, 9, 9) : """ x""",
(270, 1216, 68, 14) : """
radius 6""",
(819, 760, 140, 19) : """8] is remarkable.""",
(269, 629, 498, 19) : """
the \ufb01rst layers of every octave is relatively large. Fig. 2 (l""",
(270, 1288, 39, 14) : """
scale""",
(803, 1264, 157, 14) : """ed at that current""",
(795, 522, 164, 16) : """g the size of the de-""",
(270, 1144, 503, 18) : """
In order to be invariant to rotation, we identify a reproduci""",
(794, 1168, 166, 17) : """r-wavelet responses""",
(270, 1311, 525, 18) : """
use again integral images for fast \ufb01ltering. Only six operat""",
(270, 654, 501, 18) : """
of the detected interest points using our 'Fast-Hessian' de""",
(922, 1245, 7, 9) : """ s""",
(270, 1001, 548, 18) : """
Furthermore, we also propose an upright version of our descr""",
(340, 1221, 7, 9) : """s""",
(780, 857, 70, 18) : """ changes.""",
(270, 809, 512, 18) : """
lated features seems to yield good distinctive power while f""",
(270, 833, 527, 18) : """
of localisation errors in terms of scale or space. Using rela""",
(270, 187, 387, 16) : """6 H. Bay, T. Tuytelaars, and L. Van Gool""",
(318, 1293, 7, 9) : """ s""",
(799, 833, 160, 18) : """tive strengths and""",
(906, 1192, 55, 14) : """ood of""",
(270, 953, 535, 18) : """
Then, we construct a square region aligned to the selected or""",
(783, 785, 176, 18) : """ution of gradient re-""",
(270, 905, 503, 17) : """
plexity stripped down even further. The \ufb01rst step consists o""",
(820, 1000, 138, 19) : """iptor (U-SURF)""",
(270, 1264, 531, 18) : """
keeping with the rest, also the wavelet responses are comput""",
(270, 785, 511, 18) : """
Its mixing of crudely localised information and the distrib""",
(782, 809, 177, 18) : """ending o\ufb00 the e\ufb00ects""",
(807, 953, 152, 17) : """ientation, and ex-""",
(270, 760, 547, 19) : """
The good performance of SIFT compared to other descriptors [""",
(772, 655, 55, 13) : """tector.""",
(328, 1287, 506, 19) : """. Accordingly, at high scales the size of the wavelets is big.""",
(356, 1216, 268, 17) : """ around the interest point, with""",
(353, 1197, 9, 12) : """ y""",
(632, 1221, 7, 9) : """ s""",
(818, 1025, 141, 17) : """ to compute and""",
(797, 1312, 162, 14) : """ions are needed to""",
(844, 881, 115, 17) : """, with a com-""",
(820, 479, 140, 12) : """d of scenes shows""",
(774, 1144, 185, 14) : """ble orientation for the""",
(270, 929, 499, 18) : """
orientation based on information from a circular region aro""",
(270, 713, 244, 21) : """
4 SURF Descriptor""",
(371, 1192, 534, 18) : """ direction, shown in Fig. 2, and this in a circular neighbourh""",
(771, 929, 188, 17) : """und the interest point.""",
(270, 1048, 522, 18) : """
better suited for applications where the camera remains mor""",
(775, 905, 185, 18) : """f \ufb01xing a reproducible""",
(794, 1049, 165, 13) : """e or less horizontal.""",
(768, 629, 191, 19) : """eft) shows an example""",
(270, 1106, 289, 18) : """
4.1 Orientation Assignment""",
(746, 501, 213, 12) : """tors. Middle: Haar wavelet""",
(932, 1240, 28, 14) : """. In""",
(332, 479, 487, 15) : """ Left: Detected interest points for a Sun\ufb02ower \ufb01eld. This kin""",
(270, 500, 475, 16) : """
clearly the nature of the features from Hessian-based detec""",
(269, 977, 564, 17) : """
tract the SURF descriptor from it. These two steps are now exp""",
(300, 881, 541, 17) : """
The proposed SURF descriptor is based on similar properties""",
(269, 1239, 543, 19) : """
was detected. Also the sampling step is scale dependent and c""",
(843, 1288, 116, 17) : """ Therefore, we""",
(813, 1240, 99, 14) : """hosen to be""",
(270, 479, 53, 15) : """
Fig.2.""",
(270, 544, 277, 16) : """
scriptor window at di\ufb00erent scales.""",
(647, 1216, 312, 17) : """ the scale at which the interest point""",
(269, 522, 525, 16) : """
types used for SURF. Right: Detail of the Gra\ufb03ti scene showin""",
(270, 1168, 522, 17) : """
interest points. For that purpose, we \ufb01rst calculate the Haa""",
(270, 1193, 15, 13) : """
in""",
(314, 1192, 30, 14) : """ and""",
},
6 : {
(270, 1025, 525, 18) : """
formation about the polarity of the intensity changes, we al""",
(629, 1300, 7, 8) : """
y""",
(671, 1049, 30, 14) : """ and""",
(270, 738, 205, 18) : """
are illustrated in Fig. 2.""",
(540, 242, 9, 12) : """ y""",
(637, 1049, 9, 14) : """d""",
(487, 1108, 2, 5) : """,""",
(269, 834, 60, 13) : """
we call""",
(269, 856, 423, 19) : """
wavelet response in vertical direction (\ufb01lter size 2""",
(341, 929, 9, 14) : """ d""",
(270, 954, 120, 16) : """
interest point.""",
(494, 242, 9, 9) : """ x""",
(663, 719, 7, 9) : """s""",
(761, 930, 29, 13) : """ = 3""",
(953, 410, 7, 9) : """e""",
(270, 357, 518, 18) : """
response strength along the ordinate. The dominant orienta""",
(793, 941, 2, 2) : """.""",
(778, 1120, 181, 14) : """nt to a bias in illumi-""",
(408, 1107, 7, 8) : """y""",
(951, 1097, 8, 13) : """4""",
(270, 500, 512, 18) : """
dominating wavelet responses, large sizes yield maxima in v""",
(775, 452, 185, 18) : """ of the sliding window""",
(300, 285, 516, 18) : """
Once the wavelet responses are calculated and weighted with""",
(458, 809, 498, 18) : """5 regularly spaced sample points. For reasons of simplicity""",
(270, 1102, 11, 8) : """
v""",
(296, 314, 7, 9) : """s""",
(814, 1192, 145, 17) : """nctively di\ufb00erent""",
(270, 1120, 506, 18) : """
sub-regions of length 64. The wavelet responses are invaria""",
(389, 273, 2, 2) : """.""",
(673, 714, 287, 18) : """. Examples of such square regions""",
(460, 1097, 9, 14) : """d""",
(270, 714, 390, 17) : """
is not necessary. The size of this window is 20""",
(566, 1285, 6, 9) : """2""",
(766, 1144, 193, 18) : """chieved by turning the""",
(351, 1107, 7, 6) : """x""",
(779, 882, 181, 13) : """entation. To increase""",
(619, 1288, 9, 14) : """ d""",
(928, 291, 10, 8) : """\u03c3""",
(270, 333, 519, 18) : """
space with the horizontal response strength along the absci""",
(554, 1095, 376, 19) : """). This results in a descriptor vector for all 4""",
(270, 429, 577, 17) : """
summed. The two summed responses then yield a new vector. The""",
(430, 1095, 18, 19) : """
P""",
(798, 930, 8, 13) : """3""",
(270, 934, 63, 12) : """
sponses""",
(743, 934, 10, 8) : """\u03c3""",
(288, 1095, 26, 19) : """ = (""",
(442, 814, 9, 9) : """x""",
(383, 405, 8, 6) : """ \u03c0""",
(269, 261, 107, 14) : """
wavelets is 4""",
(559, 237, 400, 18) : """ direction at any scale. The side length of the""",
(305, 308, 500, 19) : """) centered at the interest point, the responses are represen""",
(781, 786, 179, 17) : """n, we compute a few""",
(270, 1001, 567, 14) : """
and form a \ufb01rst set of entries to the feature vector. In order t""",
(398, 1097, 9, 14) : """
d""",
(374, 1095, 18, 19) : """
P""",
(300, 1192, 513, 18) : """
Fig. 3 shows the properties of the descriptor for three disti""",
(270, 1168, 249, 17) : """
descriptor into a unit vector.""",
(270, 642, 528, 17) : """
For the extraction of the descriptor, the \ufb01rst step consists""",
(269, 548, 244, 17) : """
the U-SURF skips this step.""",
(300, 977, 244, 17) : """
Then, the wavelet responses""",
(856, 429, 104, 17) : """ longest such""",
(647, 977, 314, 18) : """ are summed up over each subregion""",
(763, 690, 198, 17) : """on, this transformation""",
(269, 690, 492, 18) : """
tion selected in the previous section. For the upright versi""",
(270, 524, 509, 17) : """
not outspoken. Both result in an unstable orientation of the""",
(270, 1216, 536, 18) : """
image intensity patterns within a subregion. One can imagin""",
(787, 905, 172, 17) : """ation errors, the re-""",
(270, 605, 289, 17) : """
4.2 Descriptor Components""",
(882, 834, 78, 13) : """ the Haar""",
(581, 977, 30, 14) : """ and""",
(270, 1143, 494, 19) : """
nation (o\ufb00set). Invariance to contrast (a scale factor) is a""",
(270, 666, 505, 18) : """
square region centered around the interest point, and orien""",
(339, 834, 9, 14) : """ d""",
(744, 1049, 217, 17) : """. Hence, each sub-region""",
(718, 1049, 9, 14) : """d""",
(817, 928, 142, 19) : """) centered at the""",
(712, 766, 9, 9) : """ x""",
(419, 1108, 2, 5) : """,""",
(630, 988, 7, 8) : """y""",
(789, 357, 171, 17) : """tion is estimated by""",
(808, 934, 7, 9) : """s""",
(865, 844, 7, 8) : """y""",
(482, 1095, 1, 19) : """|""",
(341, 1097, 9, 14) : """
d""",
(855, 834, 9, 14) : """ d""",
(581, 1288, 30, 14) : """ and""",
(730, 762, 229, 18) : """ 4 square sub-regions. This""",
(498, 1095, 18, 19) : """
P""",
(281, 321, 2, 2) : """.""",
(553, 977, 9, 14) : """ d""",
(806, 1216, 155, 14) : """e combinations of""",
(797, 1025, 163, 14) : """so extract the sum""",
(406, 929, 9, 14) : """ d""",
(270, 1240, 485, 18) : """
such local intensity patterns, resulting in a distinctive d""",
(270, 1072, 347, 18) : """
has a four-dimensional descriptor vector""",
(805, 476, 155, 18) : """ sizes \ufb01re on single""",
(805, 309, 154, 14) : """ted as vectors in a""",
(269, 453, 498, 17) : """
vector lends its orientation to the interest point. The size""",
(384, 416, 6, 9) : """
3""",
(640, 1287, 320, 19) : """, higher-order wavelets, PCA, median""",
(769, 1312, 190, 17) : """e proposed sets turned""",
(822, 284, 104, 19) : """ a Gaussian (""",
(695, 862, 7, 9) : """s""",
(433, 928, 308, 19) : """ are \ufb01rst weighted with a Gaussian (""",
(786, 525, 173, 17) : """ interest region. Note""",
(417, 940, 7, 8) : """y""",
(601, 187, 359, 15) : """SURF: Speeded Up Robust Features 7""",
(528, 1097, 9, 14) : """d""",
(286, 310, 7, 13) : """5""",
(784, 500, 176, 18) : """ector length that are""",
(563, 988, 7, 6) : """x""",
(757, 1240, 79, 17) : """escriptor.""",
(728, 1059, 7, 8) : """y""",
(556, 1288, 9, 14) : """ d""",
(850, 1264, 110, 14) : """d with fewer""",
(549, 1095, 1, 19) : """|""",
(349, 844, 7, 6) : """x""",
(633, 1047, 1, 19) : """ |""",
(396, 405, 555, 17) : """. The horizontal and vertical responses within the window ar""",
(269, 1312, 499, 17) : """
values, average values, etc. From a thorough evaluation, th""",
(644, 1072, 316, 18) : """ for its underlying intensity structure""",
(790, 333, 170, 14) : """ssa and the vertical""",
(270, 476, 527, 18) : """
is a parameter, which has been chosen experimentally. Small""",
(352, 940, 7, 6) : """x""",
(270, 881, 508, 17) : """
here is de\ufb01ned in relation to the selected interest point ori""",
(514, 242, 16, 9) : """ or""",
(705, 856, 253, 19) : """). \u201dHorizontal\u201d and \u201dvertical\u201d""",
(946, 292, 13, 4) : """ =""",
(269, 905, 516, 18) : """
the robustness towards geometric deformations and localis""",
(524, 1095, 1, 19) : """
|""",
(362, 1108, 2, 5) : """,""",
(270, 1288, 279, 18) : """
and more wavelet features, using""",
(270, 405, 101, 18) : """
an angle of""",
(367, 834, 477, 17) : """ the Haar wavelet response in horizontal direction and""",
(270, 1048, 350, 18) : """
of the absolute values of the responses,""",
(538, 1107, 7, 8) : """y""",
(776, 666, 184, 18) : """ted along the orienta-""",
(270, 310, 7, 13) : """
2""",
(379, 266, 7, 9) : """s""",
(456, 1095, 1, 19) : """
|""",
(839, 1001, 120, 18) : """o bring in in-""",
(300, 1264, 548, 17) : """
In order to arrive at these SURF descriptors, we experimente""",
(317, 1095, 18, 19) : """
P""",
(714, 1047, 1, 19) : """ |""",
(620, 977, 9, 14) : """ d""",
(647, 1059, 7, 6) : """x""",
(368, 929, 30, 14) : """ and""",
(769, 381, 192, 18) : """ation window covering""",
(470, 1107, 7, 6) : """x""",
(270, 237, 215, 17) : """
compute the response in""",
(270, 381, 497, 18) : """
calculating the sum of all responses within a sliding orient""",
(270, 786, 509, 18) : """
keeps important spatial information in. For each sub-regio""",
(625, 1078, 11, 8) : """ v""",
(629, 1285, 6, 9) : """2""",
(739, 1047, 1, 19) : """|""",
(659, 1047, 1, 19) : """|""",
(270, 809, 165, 18) : """
simple features at 5""",
(957, 821, 2, 5) : """,""",
(566, 1300, 7, 6) : """
x""",
(936, 1101, 9, 9) : """x""",
(300, 762, 402, 18) : """
The region is split up regularly into smaller 4""",
(809, 642, 150, 18) : """ of constructing a""",
},
7 : {
(270, 506, 298, 16) : """
Middle: In presence of frequencies in""",
(810, 506, 8, 12) : """d""",
(270, 695, 537, 17) : """
subdivisions appeared to be less robust and would increase m""",
(715, 1267, 243, 15) : """ased matching strategy. Right:""",
(270, 1201, 487, 15) : """
of 30 degrees, compared to the current descriptors. The inte""",
(781, 504, 18, 19) : """
P""",
(294, 550, 8, 12) : """
d""",
(330, 1157, 30, 13) : """ The""",
(269, 1223, 472, 16) : """
with our 'Fast Hessian' detector. Note that the interest poi""",
(544, 1157, 415, 16) : """ graph for di\ufb00erent binning methods and two di\ufb00erent""",
(750, 485, 208, 15) : """l values are relatively low.""",
(730, 1288, 8, 17) : """).""",
(806, 505, 1, 17) : """
|""",
(744, 1178, 216, 17) : """ 1 and 3) with a view change""",
(830, 505, 1, 17) : """|""",
(366, 1157, 40, 13) : """ recall""",
(270, 719, 459, 17) : """
much. On the other hand, the short descriptor with 3""",
(319, 550, 28, 13) : """ and""",
(743, 1223, 215, 12) : """nts are not a\ufb03ne invariant.""",
(270, 1178, 467, 17) : """
matching strategies tested on the 'Gra\ufb03ti' sequence (image""",
(411, 1162, 19, 8) : """ vs.""",
(269, 1267, 444, 15) : """
to the extended descriptor. Left: Similarity-threshold-b""",
(270, 743, 534, 18) : """
performs worse, but allows for very fast matching and is stil""",
(394, 559, 6, 5) : """x""",
(380, 549, 1, 17) : """
|""",
(303, 559, 6, 5) : """x""",
(785, 528, 175, 16) : """ direction, both values""",
(333, 462, 479, 16) : """ The descriptor entries of a sub-region represent the nature""",
(270, 1288, 457, 17) : """
Nearest-neighbour-ratio matching strategy (See section 5""",
(270, 1244, 513, 17) : """
The results are therefore not comparable to the ones in [8]. S""",
(745, 529, 14, 12) : """ in""",
(270, 767, 510, 18) : """
in comparison to other descriptors in the literature. Fig. 4""",
(809, 647, 150, 18) : """s and sub-regions.""",
(270, 1157, 53, 16) : """
Fig.4.""",
(841, 506, 119, 16) : """ is high, but all""",
(809, 695, 150, 18) : """atching times too""",
(323, 675, 9, 9) : """x""",
(819, 515, 6, 5) : """x""",
(355, 548, 18, 19) : """
P""",
(821, 462, 139, 16) : """ of the underlying""",
(414, 550, 68, 16) : """ are high.""",
(793, 789, 26, 19) : """ly).""",
(404, 549, 1, 17) : """|""",
(594, 506, 178, 16) : """ direction, the value of""",
(270, 647, 537, 17) : """
out to perform best. We then varied the number of sample point""",
(440, 1156, 97, 17) : """ (1-precision)""",
(829, 671, 130, 18) : """onsidering \ufb01ner""",
(768, 533, 9, 8) : """ x""",
(270, 187, 387, 16) : """8 H. Bay, T. Tuytelaars, and L. Van Gool""",
(806, 743, 154, 17) : """l quite acceptable""",
(270, 671, 47, 14) : """
The 4""",
(269, 789, 522, 19) : """
these comparison results (SURF-128 will be explained short""",
(790, 767, 171, 17) : """ shows only a few of""",
(576, 511, 9, 8) : """ x""",
(270, 548, 18, 19) : """ P""",
(753, 718, 205, 19) : """3 subregions (SURF-36)""",
(785, 1245, 175, 15) : """URF-128 corresponds""",
(759, 1201, 201, 15) : """rest points are computed""",
(270, 484, 479, 16) : """
intensity pattern. Left: In case of a homogeneous region, al""",
(270, 528, 467, 16) : """
others remain low. If the intensity is gradually increasing""",
(337, 671, 490, 18) : """4 sub-region division solution provided the best results. C""",
(737, 723, 9, 9) : """x""",
(384, 550, 8, 12) : """d""",
(270, 462, 53, 16) : """
Fig.3.""",
},
8 : {
(507, 309, 9, 14) : """ d""",
(270, 309, 118, 17) : """
separately for""",
(830, 284, 1, 19) : """|""",
(270, 260, 538, 19) : """
couple of similar features (SURF-128). It again uses the sam""",
(270, 883, 511, 17) : """
application. All detectors and descriptors in the comparis""",
(767, 980, 6, 9) : """ 3""",
(299, 237, 549, 17) : """
We also tested an alternative version of the SURF descriptor""",
(270, 782, 291, 20) : """
5 Experimental Results""",
(823, 1150, 136, 18) : """ in both images,""",
(798, 597, 163, 18) : """tures. The sign of""",
(793, 621, 167, 14) : """ds from the reverse""",
(270, 669, 547, 18) : """
already computed during the detection phase. In the matchin""",
(270, 452, 479, 19) : """
Mikolajczyk [8], as it contains out-of-plane rotation, in-""",
(751, 453, 209, 17) : """plane rotation as well as""",
(300, 405, 549, 18) : """
In Figure 4, the parameter choices are compared for the stand""",
(720, 481, 9, 9) : """ x""",
(782, 309, 9, 14) : """ d""",
(269, 573, 528, 19) : """
the trace of the Hessian matrix) for the underlying interest""",
(270, 907, 313, 18) : """
original implementations of authors.""",
(851, 405, 108, 15) : """ard 'Gra\ufb03ti'""",
(849, 549, 110, 19) : """aplacian (i.e.""",
(808, 285, 9, 14) : """d""",
(783, 835, 176, 14) : """oth the detector and""",
(270, 333, 242, 18) : """
up according to the sign of""",
(398, 309, 9, 14) : """ d""",
(270, 958, 179, 15) : """
Standard Evaluation""",
(269, 1030, 532, 17) : """
the results on all sequences. For the detector comparison, w""",
(300, 549, 546, 18) : """
For fast indexing during the matching stage, the sign of the L""",
(533, 1312, 162, 17) : """vgg/research/a\ufb03ne/""",
(270, 1006, 518, 17) : """
real textured and structured scenes. Due to space limitatio""",
(790, 1006, 170, 17) : """ns, we cannot show""",
(270, 357, 549, 17) : """
descriptor is more distinctive and not much slower to comput""",
(856, 309, 9, 14) : """d""",
(275, 1310, 5, 8) : """
3""",
(785, 1173, 174, 19) : """ (where only the part""",
(802, 1030, 157, 14) : """e selected the two""",
(805, 1053, 155, 19) : """Boat) and lighting""",
(817, 669, 143, 18) : """g stage, we only""",
(270, 717, 498, 18) : """
information allows for faster matching and gives a slight in""",
(524, 1319, 6, 1) : """\u02dc""",
(877, 308, 1, 19) : """|""",
(270, 285, 458, 17) : """
but now splits these values up further. The sums of""",
(769, 717, 190, 17) : """crease in performance.""",
(601, 187, 358, 15) : """SURF: Speeded Up Robust Features 9""",
(558, 309, 216, 17) : """ 0. Similarly, the sums of""",
(776, 982, 185, 18) : """. These are images of""",
(520, 333, 9, 14) : """ d""",
(270, 1077, 525, 19) : """
changes (Leuven) (see Fig. 6, discussed below). The descrip""",
(300, 1127, 521, 17) : """
For the detectors, we use the repeatability score, as descri""",
(408, 320, 7, 8) : """y""",
(270, 835, 511, 17) : """
First, we present results on a standard evaluation set, fot b""",
(269, 1053, 533, 19) : """
viewpoint changes (Gra\ufb03ti and Wall), one zoom and rotation (""",
(795, 645, 165, 17) : """nal cost, as it was""",
(517, 320, 7, 8) : """y""",
(270, 1101, 543, 19) : """
shown for all sequences except the Bark sequence (see Fig. 4 a""",
(745, 296, 7, 6) : """x""",
(270, 982, 488, 18) : """
sequences and testing software provided by Mikolajczyk""",
(735, 285, 9, 14) : """ d""",
(792, 320, 7, 8) : """y""",
(872, 1223, 88, 17) : """etector by""",
(270, 693, 556, 17) : """
compare features if they have the same type of contrast. Henc""",
(821, 357, 138, 17) : """e, but slower to""",
(810, 309, 30, 14) : """ and""",
(426, 312, 12, 11) : """ <""",
(807, 574, 152, 17) : """ point is included.""",
(270, 381, 339, 18) : """
match due to its higher dimensionality.""",
(449, 309, 48, 14) : """ 0 and""",
(270, 501, 569, 17) : """
comes out to perform best. Also, SURF performs well and is fas""",
(804, 284, 1, 19) : """ |""",
(270, 597, 527, 18) : """
Typically, the interest points are found at blob-type struc""",
(857, 237, 102, 14) : """ that adds a""",
(270, 525, 396, 18) : """
Both outperform the existing state-of-the-art.""",
(808, 1247, 151, 17) : """posed by Mikola-""",
(535, 310, 12, 15) : """ \u2265""",
(841, 501, 118, 14) : """ter to handle.""",
(819, 296, 7, 6) : """x""",
(270, 1174, 505, 17) : """
relative to the lowest total number of interest points found""",
(269, 621, 523, 18) : """
the Laplacian distinguishes bright blobs on dark backgroun""",
(463, 959, 497, 17) : """ We tested our detector and descriptor using the image""",
(270, 1246, 536, 19) : """
Lowe [2], and the Harris- and Hessian-Laplace detectors pro""",
(797, 1078, 163, 14) : """tor evaluations are""",
(773, 859, 188, 18) : """life object recognition""",
(827, 693, 133, 17) : """e, this minimal""",
(842, 285, 117, 17) : """ are computed""",
(824, 429, 137, 14) : """valuation set of""",
(783, 883, 176, 14) : """on are based on the""",
(270, 645, 523, 17) : """
situation. This feature is available at no extra computatio""",
(808, 1197, 29, 19) : """nt).""",
(866, 320, 7, 8) : """y""",
(269, 859, 502, 17) : """
the descriptor. Next, we discuss results obtained in a real-""",
(763, 285, 30, 14) : """ and""",
(270, 1198, 537, 18) : """
of the image that is visible in both images is taken into accou""",
(270, 477, 440, 18) : """
brightness changes. The extended descriptor for 4""",
(300, 1222, 571, 19) : """
The detector is compared to the di\ufb00erence of Gaussian (DoG) d""",
(802, 1270, 158, 18) : """ very similar for all""",
(530, 344, 7, 6) : """x""",
(814, 1101, 50, 19) : """nd 7).""",
(738, 476, 220, 19) : """ 4 subregions (SURF-128)""",
(268, 1269, 527, 19) : """
jczyk [15]. The number of interest points found is on average""",
(852, 308, 1, 19) : """ |""",
(809, 261, 150, 17) : """e sums as before,""",
(541, 333, 418, 18) : """, thereby doubling the number of features. The""",
(822, 1125, 137, 19) : """bed in [9]. This""",
(290, 1312, 231, 17) : """ http://www.robots.ox.ac.uk/""",
(270, 1150, 543, 18) : """
indicates how many of the detected interest points are found""",
(270, 429, 552, 18) : """
scene, which is the most challenging of all the scenes in the e""",
(889, 309, 70, 17) : """ are split""",
},
9 : {
(269, 428, 325, 15) : """
the overall robustness of the features.""",
(787, 237, 173, 14) : """he database used in""",
(851, 477, 108, 17) : """he sequence,""",
(270, 237, 515, 18) : """
detectors. This holds for all images, including those from t""",
(270, 332, 528, 19) : """
is comparable (Gra\ufb03ti, Leuven, Boats) or even better (Wall)""",
(794, 716, 165, 18) : """ Fig. 7, as this tech-""",
(771, 739, 188, 17) : """escriptor in its feature""",
(396, 1159, 100, 13) : """
Fast-Hessian""",
(414, 1137, 64, 12) : """
detector""",
(541, 1160, 25, 12) : """ 600""",
(879, 499, 80, 19) : """ 1 and 5),""",
(802, 596, 157, 18) : """ons. In Fig. 4, we""",
(808, 285, 151, 14) : """ DoG and 5 times""",
(270, 357, 526, 17) : """
petitors. Note that the sequences Gra\ufb03ti and Wall contain ou""",
(853, 883, 106, 14) : """herefore less""",
(536, 1204, 34, 12) : """ 2500""",
(705, 1292, 8, 8) : """ x""",
(270, 762, 332, 19) : """
space [8] and it is in more general use.""",
(270, 1047, 555, 18) : """
aimed at recognising objects of art in a museum. The database""",
(269, 261, 537, 18) : """
the object recognition experiment, see Table 1 for an exampl""",
(270, 548, 584, 17) : """
ures 4 and 7, we compared our SURF descriptor to GLOH, SIFT and""",
(270, 476, 579, 18) : """
For each evaluation, we used the \ufb01rst and the fourth image of t""",
(537, 1182, 33, 12) : """ 1000""",
(269, 978, 571, 19) : """
timings were evaluated on a standard Linux PC (Pentium IV, 3G""",
(843, 1072, 116, 14) : """ere taken un-""",
(721, 1288, 32, 17) : """ 640)""",
(270, 858, 534, 19) : """
The accurate version (SURF-128), presented in section 4, sh""",
(834, 1047, 126, 15) : """ consists of 216""",
(817, 643, 143, 19) : """ ratio (see [8] for""",
(270, 1288, 426, 17) : """
in our comparison. (First image of Gra\ufb03ti scene, 800""",
(628, 1182, 34, 12) : """ 1979""",
(269, 883, 582, 18) : """
ter results than the regular SURF, but is slower to match and t""",
(270, 716, 516, 18) : """
results on similarity threshold based matching are shown in""",
(300, 452, 464, 19) : """
The descriptors are evaluated using recall-(1-precision)""",
(797, 357, 162, 17) : """t-of-plane rotation,""",
(806, 692, 154, 17) : """e limitations, only""",
(517, 1137, 73, 12) : """ threshold""",
(270, 405, 510, 17) : """
rotation- and scale invariant. Hence, these deformations h""",
(270, 1071, 572, 19) : """
images of 22 objects. The images of the test set (116 images) w""",
(270, 620, 523, 18) : """
compared the results using two di\ufb00erent matching technique""",
(300, 787, 537, 17) : """
The SURF descriptor outperforms the other descriptors in a s""",
(597, 1136, 95, 16) : """ nb of points""",
(270, 572, 519, 17) : """
based on interest points detected with our 'Fast-Hessian' d""",
(760, 1182, 26, 12) : """ 650""",
(628, 1159, 34, 13) : """ 1418""",
(628, 1203, 34, 13) : """ 1664""",
(270, 667, 549, 19) : """
a discussion on these techniques). This has an e\ufb00ect on the ra""",
(269, 954, 579, 19) : """
we always use the same set of parameters and thresholds (see t""",
(270, 596, 531, 17) : """
performed the other descriptors for almost all the comparis""",
(300, 931, 514, 18) : """
Note that throughout the paper, including the object recogn""",
(270, 835, 552, 17) : """
same level of precision. At the same time, it is fast to comput""",
(782, 405, 178, 17) : """ave to be tackled by""",
(270, 739, 499, 17) : """
nique is better suited to represent the distribution of the d""",
(270, 691, 534, 18) : """
scriptors, yet SURF performed best in both cases. Due to spac""",
(814, 931, 145, 17) : """ition experiment,""",
(839, 787, 120, 18) : """ystematic and""",
(442, 1023, 517, 18) : """ We also tested the new features on a practical application,""",
(787, 309, 173, 17) : """ility for our detector""",
(847, 811, 112, 14) : """ recall for the""",
(824, 834, 135, 19) : """e (see Table 2).""",
(791, 572, 168, 14) : """etector. SURF out-""",
(270, 1267, 70, 12) : """
Table 1.""",
(795, 620, 164, 17) : """s, one based on the""",
(830, 1266, 130, 13) : """ for the detectors""",
(820, 668, 139, 18) : """nking of the de-""",
(270, 644, 537, 18) : """
similarity threshold and one based on the nearest neighbour""",
(628, 1225, 33, 12) : """ 1520""",
(819, 524, 140, 18) : """pectively. In \ufb01g-""",
(271, 187, 386, 16) : """10 H. Bay, T. Tuytelaars, and L. Van Gool""",
(861, 548, 98, 17) : """ PCA-SIFT,""",
(757, 1204, 33, 12) : """ 1800""",
(808, 261, 152, 14) : """e. As can be seen""",
(808, 333, 151, 14) : """ than for the com-""",
(771, 452, 198, 19) : """graphs, as in [4] and [8].""",
(272, 1023, 159, 18) : """
Object Recognition""",
(699, 1136, 147, 17) : """ comp. time (msec)""",
(526, 1225, 53, 12) : """ default""",
(842, 978, 35, 19) : """Hz).""",
(270, 524, 547, 18) : """
corresponding to a viewpoint change of 30 and 50 degrees, res""",
(428, 1225, 35, 13) : """
DoG""",
(805, 859, 154, 18) : """owed slightly bet-""",
(270, 907, 387, 18) : """
interesting for speed-dependent applications.""",
(270, 499, 597, 19) : """
except for the Gra\ufb03ti (image 1 and 3) and the Wall scene (image""",
(270, 810, 568, 19) : """
signi\ufb01cant way, with sometimes more than 10% improvement in""",
(348, 1266, 475, 16) : """ Thresholds, number of detected points and calculation time""",
(382, 1181, 128, 16) : """
Hessian-Laplace""",
(794, 381, 166, 17) : """omparison are only""",
(761, 1160, 25, 12) : """ 120""",
(388, 1203, 116, 16) : """
Harris-Laplace""",
(270, 309, 515, 17) : """
faster than Hessian-Laplace. At the same time, the repeatab""",
(760, 1225, 26, 12) : """ 400""",
(270, 381, 522, 18) : """
resulting in a\ufb03ne deformations, while the detectors in the c""",
(850, 954, 109, 19) : """able 1). The""",
(270, 285, 528, 14) : """
our 'Fast-Hessian' detector is more than 3 times faster that""",
},
10 : {
(807, 948, 153, 19) : """ (SIFT) and 72.3%""",
(605, 235, 48, 13) : """ SURF""",
(270, 782, 519, 14) : """
if its distance is closer than 0.7 times the distance of the se""",
(269, 1290, 315, 15) : """
the di\ufb00erence in viewpoint and colours.""",
(843, 710, 117, 18) : """he test image""",
(270, 628, 525, 18) : """
matching their respective interest points. The object show""",
(271, 948, 527, 19) : """
(82.6%). The other descriptors achieve 78.3% (GLOH), 78.1%""",
(270, 546, 318, 17) : """
recognition, as many details get lost.""",
(818, 734, 141, 18) : """culating the Eu-""",
(753, 258, 33, 12) : """ 1036""",
(270, 604, 575, 18) : """
The images in the test set are compared to all images in the ref""",
(270, 877, 554, 18) : """
make sense, as these may hide shortcomings of the basic schem""",
(814, 299, 146, 16) : """mentations, tested""",
(551, 258, 25, 12) : """ 255""",
(769, 474, 191, 18) : """s, objects in re\ufb02ecting""",
(270, 734, 546, 18) : """
is compared to an interest point in the reference image by cal""",
(347, 299, 466, 16) : """ Computation times for the joint detector - descriptor imple""",
(786, 758, 173, 18) : """ing pair is detected,""",
(300, 710, 541, 18) : """
The matching is carried out as follows. An interest point in t""",
(270, 901, 505, 18) : """
recognition rates re\ufb02ect the results of our performance eva""",
(270, 651, 582, 18) : """
image with the highest number of matches with respect to the t""",
(777, 901, 182, 14) : """luation. The leader is""",
(270, 497, 524, 18) : """
glass cabinets, viewpoint changes, zoom, di\ufb00erent camera q""",
(854, 652, 105, 17) : """est image is""",
(844, 580, 115, 14) : """ed as follows.""",
(766, 830, 193, 17) : """e positive matches, yet""",
(844, 1267, 116, 17) : """t (right). Note""",
(616, 258, 26, 12) : """ 354""",
(797, 628, 163, 14) : """n on the reference""",
(270, 806, 513, 18) : """
bour. This is the nearest neighbour ratio matching strategy""",
(440, 257, 81, 17) : """
time (ms):""",
(269, 853, 568, 18) : """
this can be done on top of any matcher. For comparing reasons,""",
(270, 321, 536, 16) : """
on the \ufb01rst image of the Gra\ufb03ti sequence. The thresholds are a""",
(846, 853, 113, 14) : """ this does not""",
(270, 758, 515, 17) : """
clidean distance between their descriptor vectors. A match""",
(601, 187, 358, 15) : """SURF: Speeded Up Robust Features 11""",
(792, 805, 167, 19) : """ [18,2,7]. Obviously,""",
(271, 972, 112, 19) : """
(PCA-SIFT).""",
(270, 520, 266, 19) : """
over, the images are small (320""",
(270, 924, 543, 19) : """
SURF-128 with 85.7% recognition rate, followed by U-SURF (8""",
(270, 365, 287, 16) : """
also representative for other images.""",
(561, 520, 398, 19) : """240) and therefore more challenging for object""",
(749, 235, 40, 13) : """ SIFT""",
(807, 321, 153, 16) : """dapted in order to""",
(826, 877, 134, 18) : """es. The average""",
(815, 924, 144, 19) : """3.8%) and SURF""",
(660, 235, 81, 13) : """ SURF-128""",
(270, 829, 494, 19) : """
additional geometric constraints reduce the impact of fals""",
(270, 1268, 53, 15) : """
Fig.5.""",
(780, 343, 180, 16) : """ese relative speeds are""",
(270, 299, 69, 13) : """
Table 2.""",
(270, 343, 508, 16) : """
detect the same number of interest points for all methods. Th""",
(795, 498, 164, 16) : """ualities, etc. More-""",
(544, 526, 9, 9) : """x""",
(688, 258, 25, 12) : """ 391""",
(300, 580, 543, 18) : """
In order to recognise the objects from the database, we proce""",
(332, 1267, 511, 17) : """ An example image from the reference set (left) and the test se""",
(270, 474, 497, 18) : """
der various conditions, including extreme lighting change""",
(270, 676, 276, 17) : """
chosen as the recognised object.""",
(791, 782, 168, 18) : """cond nearest neigh-""",
(845, 604, 114, 17) : """erence set by""",
(530, 235, 68, 13) : """
U-SURF""",
},
11 : {
(270, 1049, 194, 18) : """
Acknowledgements:""",
(270, 977, 505, 17) : """
racy. The descriptor is easily extendable for the descripti""",
(270, 953, 510, 17) : """
scheme which outperforms the current state-of-the art, bot""",
(786, 1209, 117, 13) : """lection. IJCV""",
(290, 1312, 239, 17) : """ http://www.vision.ee.ethz.ch/""",
(777, 977, 183, 14) : """on of a\ufb03ne invariant""",
(332, 748, 465, 16) : """ Repeatability score for image sequences, from left to right""",
(860, 1073, 100, 14) : """or Scienti\ufb01c""",
(541, 1312, 38, 17) : """surf/""",
(743, 1022, 6, 9) : """4""",
(801, 1000, 158, 18) : """tional speed up. A""",
(279, 1253, 461, 15) : """
2. Lowe, D.: Distinctive image features from scale-invaria""",
(913, 1208, 45, 17) : """ 30(2)""",
(476, 1049, 484, 18) : """ The authors gratefully acknowledge the support from""",
(270, 1158, 123, 17) : """
References""",
(532, 1319, 6, 1) : """\u02dc""",
(269, 769, 505, 17) : """
Wall and Gra\ufb03ti (Viewpoint Change), Leuven (Lighting Chang""",
(741, 1253, 218, 15) : """nt keypoints, cascade \ufb01lter-""",
(270, 878, 167, 16) : """
6 Conclusion""",
(775, 769, 185, 17) : """e) and Boat (Zoom and""",
(270, 1073, 590, 17) : """
Swiss SNF NCCR project IM2, Toyota-TME and the Flemish Fund f""",
(304, 1230, 122, 17) : """
(1998) 79 \u2013 116""",
(470, 1276, 19, 11) : """ 60""",
(825, 929, 136, 17) : """tion-description""",
(270, 748, 53, 16) : """
Fig.6.""",
(280, 1209, 505, 15) : """
1. Lindeberg, T.: Feature detection with automatic scale se""",
(782, 953, 177, 17) : """h in speed and accu-""",
(269, 929, 554, 17) : """
We have presented a fast and performant interest point detec""",
(270, 791, 80, 17) : """
Rotation).""",
(270, 1001, 530, 18) : """
regions. Future work will aim at optimising the code for addi""",
(270, 1097, 80, 14) : """
Research.""",
(753, 1037, 2, 2) : """.""",
(499, 1274, 121, 17) : """ (2004) 91 \u2013 110""",
(303, 1275, 159, 15) : """
ing approach. IJCV""",
(806, 748, 153, 16) : """ and top to bottom,""",
(270, 1025, 472, 17) : """
binary of the latest version is available on the internet""",
(275, 1310, 6, 8) : """
4""",
(271, 187, 386, 16) : """12 H. Bay, T. Tuytelaars, and L. Van Gool""",
},
12 : {
(270, 1274, 501, 16) : """
27. Brown, M., Lowe, D.: Invariant features from interest po""",
(303, 1253, 346, 17) : """
sentations. In: Scale-Space. (2003) 148\u2013163""",
(332, 535, 100, 17) : """ (2005) 43\u201372""",
(271, 914, 472, 17) : """
19. Scha\ufb00alitzky, F., Zisserman, A.: Multi-view matching f""",
(304, 893, 131, 17) : """
(2000) 774 \u2013 781""",
(771, 450, 189, 15) : """ local descriptors. PAMI""",
(855, 660, 45, 17) : """ 45(2)""",
(271, 641, 464, 16) : """
12. Lowe, D.: Object recognition from local scale-invarian""",
(773, 1190, 186, 16) : """e-Space Primal Sketch,""",
(303, 1170, 26, 12) : """
370""",
(303, 724, 390, 17) : """
categories. In: CVPR. Volume II. (2004) 90 \u2013 96""",
(781, 746, 177, 15) : """terest point detectors.""",
(303, 810, 453, 16) : """
intensity transformations and di\ufb00erential invariants. JM""",
(757, 281, 203, 15) : """esentation for local image""",
(772, 1274, 186, 16) : """int groups. In: BMVC.""",
(303, 1127, 331, 17) : """
features. In: CVPR (1). (2001) 511 \u2013 518""",
(771, 853, 19, 11) : """ 94""",
(304, 429, 283, 17) : """
CVPR. Volume 2. (2003) 257 \u2013 263""",
(743, 915, 217, 15) : """or unordered image sets, or""",
(814, 514, 146, 13) : """n detectors. IJCV""",
(270, 1148, 492, 16) : """
24. Koenderink, J.: The structure of images. Biological Cyb""",
(303, 387, 478, 17) : """
mally stable extremal regions. In: BMVC. (2002) 384 \u2013 393""",
(303, 514, 510, 16) : """
itzky, F., Kadir, T., Van Gool, L.: A comparison of a\ufb03ne regio""",
(271, 788, 475, 16) : """
16. Florack, L.M.J., Haar Romeny, B.M.t., Koenderink, J.J.""",
(757, 810, 20, 12) : """IV""",
(270, 1190, 502, 16) : """
25. Lindeberg, T.: Discrete Scale-Space Theory and the Scal""",
(779, 1042, 179, 15) : """ modeling and localiza-""",
(764, 239, 194, 13) : """oint detector. In: ECCV.""",
(271, 661, 491, 16) : """
13. Kadir, T., Brady, M.: Scale, saliency and image descript""",
(799, 851, 91, 17) : """ (2004) 3\u201327""",
(764, 1148, 61, 12) : """ernetics""",
(279, 323, 485, 16) : """
5. Tuytelaars, T., Van Gool, L.: Wide baseline stereo based o""",
(304, 260, 131, 17) : """
(2002) 128 \u2013 142""",
(303, 577, 394, 17) : """
of the Alvey Vision Conference. (1988) 147 \u2013 151""",
(304, 472, 19, 12) : """
27""",
(305, 936, 534, 17) : """
\u201cHow do I organize my holiday snaps?\u201d. In: ECCV. Volume 1. (20""",
(303, 768, 42, 13) : """
IJCV""",
(772, 1063, 188, 13) : """rnational Astronautical""",
(741, 1232, 218, 16) : """ in hybrid multi-scale repre-""",
(279, 365, 512, 16) : """
6. Matas, J., Chum, O., M., U., Pajdla, T.: Robust wide baseli""",
(303, 620, 277, 17) : """
ICCV. Volume 1. (2001) 525 \u2013 531""",
(763, 703, 196, 16) : """or recognition of object""",
(861, 1147, 100, 17) : """ (1984) 363 \u2013""",
(304, 1084, 125, 17) : """
Congress (2004)""",
(304, 1296, 47, 17) : """
(2002)""",
(785, 1105, 175, 16) : """ted cascade of simple""",
(304, 1020, 131, 17) : """
(2003) 736 \u2013 743""",
(279, 238, 484, 16) : """
3. Mikolajczyk, K., Schmid, C.: An a\ufb03ne invariant interest p""",
(748, 872, 210, 16) : """eparated views. In: CVPR.""",
(303, 684, 66, 12) : """
83 \u2013 105""",
(784, 811, 9, 11) : """ 4""",
(353, 768, 19, 11) : """ 60""",
(303, 1211, 295, 17) : """
PhD, KTH Stockholm,. KTH (1991)""",
(789, 557, 171, 15) : """ctor. In: Proceedings""",
(765, 661, 82, 13) : """ion. IJCV""",
(793, 365, 166, 13) : """ne stereo from maxi-""",
(271, 599, 487, 15) : """
11. Mikolajczyk, K., Schmid, C.: Indexing based on scale inv""",
(381, 767, 113, 17) : """ (2004) 63 \u2013 86""",
(303, 302, 355, 17) : """
descriptors. In: CVPR (2). (2004) 506 \u2013 513""",
(736, 640, 222, 17) : """t features. In: ICCV. (1999)""",
(304, 978, 131, 17) : """
(1991) 891 \u2013 906""",
(279, 450, 486, 16) : """
8. Mikolajczyk, K., Schmid, C.: A performance evaluation of""",
(791, 408, 167, 15) : """ local descriptors. In:""",
(279, 407, 504, 16) : """
7. Mikolajczyk, K., Schmid, C.: A performance evaluation of""",
(271, 703, 492, 16) : """
14. Jurie, F., Schmid, C.: Scale-invariant shape features f""",
(270, 1106, 514, 15) : """
23. Viola, P., Jones, M.: Rapid object detection using a boos""",
(271, 830, 508, 16) : """
17. Mindru, F., Tuytelaars, T., Van Gool, L., Moons, T.: Mome""",
(759, 599, 199, 15) : """ariant interest points. In:""",
(270, 1041, 500, 16) : """
22. Se, S., Ng, H., Jasiobedzki, P., Moyung, T.: Vision based""",
(271, 872, 476, 16) : """
18. Baumberg, A.: Reliable feature matching across widely s""",
(911, 660, 47, 17) : """ (2001)""",
(751, 998, 207, 17) : """l features. In: CVPR (1).""",
(303, 537, 19, 11) : """
65""",
(802, 809, 119, 17) : """ (1994) 171\u2013187""",
(771, 492, 188, 16) : """ A., Matas, J., Scha\ufb00al-""",
(279, 281, 477, 16) : """
4. Ke, Y., Sukthankar, R.: Pca-sift: A more distinctive repr""",
(303, 852, 460, 16) : """
nition under changing viewpoint and illumination. CVIU""",
(751, 788, 209, 16) : """, Viergever, M.A.: General""",
(303, 1063, 468, 16) : """
tion for planetary exploration rovers. Proceedings of Inte""",
(833, 1149, 18, 11) : """ 50""",
(787, 957, 145, 13) : """able \ufb01lters. PAMI""",
(271, 746, 509, 16) : """
15. Mikolajczyk, K., Schmid, C.: Scale and a\ufb03ne invariant in""",
(279, 492, 482, 16) : """
9. Mikolajczyk, K., Tuytelaars, T., Schmid, C., Zisserman,""",
(941, 958, 18, 11) : """ 13""",
(780, 830, 178, 16) : """nt invariants for recog-""",
(270, 1232, 463, 16) : """
26. Lindeberg, T., Bretzner, L.: Real-time scale selection""",
(841, 936, 107, 17) : """02) 414 \u2013 431""",
(601, 187, 358, 15) : """SURF: Speeded Up Robust Features 13""",
(270, 957, 515, 16) : """
20. Freeman, W.T., Adelson, E.H.: The design and use of steer""",
(303, 344, 298, 17) : """
regions. In: BMVC. (2000) 412 \u2013 422""",
(271, 556, 517, 16) : """
10. Harris, C., Stephens, M.: A combined corner and edge dete""",
(270, 999, 480, 16) : """
21. Carneiro, G., Jepson, A.: Multi-scale phase-based loca""",
(332, 471, 136, 17) : """ (2005) 1615\u20131630""",
(765, 323, 194, 16) : """n local, a\ufb03nely invariant""",
},
13 : {
(270, 1148, 482, 17) : """
point change of 50 (Wall) degrees, scale factor 2 (Boat), ima""",
(271, 187, 386, 16) : """14 H. Bay, T. Tuytelaars, and L. Van Gool""",
(842, 1127, 117, 15) : """ bottom, View-""",
(270, 1170, 470, 17) : """
brightness change (Leuven) and JPEG compression (Ubc).""",
(334, 1127, 498, 15) : """ Recall, 1-Precision graphs for, from left to right and top to""",
(270, 1127, 53, 15) : """
Fig.7.""",
(753, 1148, 206, 17) : """ge blur (Bikes and Trees),""",
}
}
class CaptionExtractorTest(unittest.TestCase):
    """regression tests about BibRecDocs"""

    def test_intersect(self):
        cb = CaptionExtractor(boxes[1], 560, 1190)
        
        self.assertEqual(cb.intersect([(0., 1.), (2., 1.), (3., 2.), (1., 3.)], \
                                      [(2., 2.), (3., 2.), (3., 4.), (2., 4.)]), \
                                      True, "Polygon intersection algorithm failed")
        self.assertEqual(cb.intersect([(0., 1.), (2., 1.), (3., 2.), (1., 3.)], \
                                      [(4., 2.), (5., 2.), (5., 3.), (4., 3.)]), \
                                      False, "Polygon intersection algorithm failed")
    
    def test_remove_non_intersecting_boxes(self):
        cb = CaptionExtractor(boxes[0], 560, 1190)
        cb.remove_non_intersecting_boxes([(0.,0.), (200, 0.), (200., 120.), (0.,120.)])
        cb.merge_near_boxes()
        self.assertEqual("SURF: Speeded Up Robust Features", cb.get_caption_text(), "Removing non intersecting boxes and text extraction failed")
   

TEST_SUITE = make_test_suite(CaptionExtractorTest)
                             

if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)



                   




