#!/usr/bin/env python3
"""
Generate static HTML pages for SEO-friendly URLs
Structure: /locations/{state}/index.html
           /locations/{state}/{city}/index.html
           /locations/{state}/{city}/{clinic-slug}.html
"""

import os
import re
import json

# Clinic database from app.js
CLINIC_DATABASE = {
    'California': {
        'Los Angeles': {
            'avgPrice': 5500,
            'clinics': [
                {'name': 'Alexander E Weber, MD', 'address': '16311 Ventura Blvd #515, Encino, CA 91436', 'phone': '(818) 658-5920', 'specialty': 'Sports Medicine & Regenerative Orthopedics', 'priceRange': '$4,000 - $8,000', 'featured': True, 'verified': True},
                {'name': 'Full Range Ortho', 'address': '310 N Westlake Blvd #200, Westlake Village, CA 91362', 'phone': '855-906-7246', 'specialty': 'Orthopedic Stem Cell Therapy', 'priceRange': '$3,500 - $7,500', 'featured': False, 'verified': True},
                {'name': 'Dr. Steve Yoon', 'address': '450 N Roxbury Dr #602, Beverly Hills, CA 90210', 'phone': '(310) 890-1411', 'specialty': 'Regenerative Sports Medicine', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True},
                {'name': 'Cedars-Sinai Kerlan-Jobe Institute', 'address': '6801 Park Terrace, Los Angeles, CA 90045', 'phone': '(310) 665-7200', 'specialty': 'Sports Medicine & Orthobiologics', 'priceRange': '$6,000 - $15,000', 'featured': True, 'verified': True},
                {'name': 'Southern California Orthopedic Institute', 'address': '6815 Noble Ave, Van Nuys, CA 91405', 'phone': '(818) 901-6600', 'specialty': 'Joint Preservation & Regenerative Medicine', 'priceRange': '$4,500 - $10,000', 'featured': False, 'verified': True}
            ]
        },
        'San Diego': {
            'avgPrice': 5200,
            'clinics': [
                {'name': 'San Diego Orthobiologics Medical Group', 'address': '6699 Alvarado Rd #2301, San Diego, CA 92120', 'phone': '(619) 286-7900', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $9,000', 'featured': True, 'verified': True},
                {'name': 'Regenerative Institute of Newport Beach', 'address': '4150 Regents Park Row #365, La Jolla, CA 92037', 'phone': '(858) 412-6800', 'specialty': 'Stem Cell Therapy', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True},
                {'name': 'San Diego Sports Medicine', 'address': '5550 Grossmont Center Dr, La Mesa, CA 91942', 'phone': '(619) 229-3932', 'specialty': 'Sports Regenerative Medicine', 'priceRange': '$3,500 - $8,000', 'featured': False, 'verified': True}
            ]
        },
        'San Jose': {
            'avgPrice': 5800,
            'clinics': [
                {'name': 'Silicon Valley Orthopedics', 'address': '2500 Hospital Dr, Mountain View, CA 94040', 'phone': '(650) 988-7400', 'specialty': 'Orthopedic Regenerative Medicine', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True},
                {'name': 'Bay Area Stem Cell Associates', 'address': '15400 Los Gatos Blvd, Los Gatos, CA 95032', 'phone': '(408) 356-4500', 'specialty': 'Stem Cell Therapy', 'priceRange': '$4,500 - $10,000', 'featured': False, 'verified': True}
            ]
        },
        'San Francisco': {
            'avgPrice': 6200,
            'clinics': [
                {'name': 'UCSF Orthopedic Institute', 'address': '1500 Owens St, San Francisco, CA 94158', 'phone': '(415) 353-2808', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$6,000 - $15,000', 'featured': True, 'verified': True},
                {'name': 'San Francisco Stem Cell Treatment Center', 'address': '450 Sutter St #840, San Francisco, CA 94108', 'phone': '(415) 432-7290', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True},
                {'name': 'Pacific Heights Orthopedics', 'address': '2100 Webster St #422, San Francisco, CA 94115', 'phone': '(415) 923-0944', 'specialty': 'Sports Medicine & PRP', 'priceRange': '$4,000 - $9,000', 'featured': False, 'verified': True}
            ]
        },
        'Fresno': {
            'avgPrice': 4500,
            'clinics': [
                {'name': 'Central Valley Orthopedics', 'address': '7077 N Fresno St, Fresno, CA 93720', 'phone': '(559) 256-5200', 'specialty': 'Regenerative Joint Care', 'priceRange': '$3,500 - $8,000', 'featured': True, 'verified': True},
                {'name': 'Fresno Stem Cell Center', 'address': '6069 N First St #103, Fresno, CA 93710', 'phone': '(559) 432-1800', 'specialty': 'Stem Cell Therapy', 'priceRange': '$4,000 - $9,000', 'featured': False, 'verified': True}
            ]
        },
        'Sacramento': {
            'avgPrice': 5000,
            'clinics': [
                {'name': 'UC Davis Health Orthopedics', 'address': '4860 Y St #3800, Sacramento, CA 95817', 'phone': '(916) 734-2798', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True},
                {'name': 'Sacramento Stem Cell Treatment', 'address': '1515 Response Rd #100, Sacramento, CA 95815', 'phone': '(916) 921-7900', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $9,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Texas': {
        'Houston': {
            'avgPrice': 4900,
            'clinics': [
                {'name': 'Houston Stem Cell Center', 'address': '6560 Fannin St #1124, Houston, TX 77030', 'phone': '(713) 800-1120', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True},
                {'name': 'Texas Orthobiologics', 'address': '7505 S Main St #350, Houston, TX 77030', 'phone': '(713) 794-3599', 'specialty': 'Orthopedic Stem Cell Therapy', 'priceRange': '$3,500 - $8,000', 'featured': True, 'verified': True},
                {'name': 'Fondren Orthopedic Group', 'address': '7401 S Main St, Houston, TX 77030', 'phone': '(713) 799-2300', 'specialty': 'Sports Medicine & Regenerative Care', 'priceRange': '$4,500 - $12,000', 'featured': False, 'verified': True},
                {'name': 'Memorial Hermann Sports Medicine', 'address': '6400 Fannin St #2600, Houston, TX 77030', 'phone': '(713) 441-3800', 'specialty': 'Academic Sports Medicine', 'priceRange': '$5,000 - $15,000', 'featured': True, 'verified': True}
            ]
        },
        'San Antonio': {
            'avgPrice': 4500,
            'clinics': [
                {'name': 'San Antonio Regenerative Medicine', 'address': '7940 Floyd Curl Dr, San Antonio, TX 78229', 'phone': '(210) 567-5000', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$3,500 - $9,000', 'featured': True, 'verified': True},
                {'name': 'Alamo Stem Cell Center', 'address': '8042 Wurzbach Rd #450, San Antonio, TX 78229', 'phone': '(210) 614-6432', 'specialty': 'Stem Cell Therapy', 'priceRange': '$4,000 - $10,000', 'featured': False, 'verified': True}
            ]
        },
        'Dallas': {
            'avgPrice': 5200,
            'clinics': [
                {'name': 'Dallas Stem Cell Treatment Center', 'address': '7777 Forest Ln #C350, Dallas, TX 75230', 'phone': '(972) 566-5500', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,500 - $12,000', 'featured': True, 'verified': True},
                {'name': 'Texas Health Orthopedics', 'address': '8200 Walnut Hill Ln, Dallas, TX 75231', 'phone': '(214) 345-4545', 'specialty': 'Orthopedic Regenerative Care', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True},
                {'name': 'Baylor Scott & White Sports Medicine', 'address': '3900 Junius St, Dallas, TX 75246', 'phone': '(214) 820-0111', 'specialty': 'Academic Sports Medicine', 'priceRange': '$5,000 - $15,000', 'featured': False, 'verified': True}
            ]
        },
        'Austin': {
            'avgPrice': 5000,
            'clinics': [
                {'name': 'Austin Stem Cell Center', 'address': '3705 Medical Pkwy #430, Austin, TX 78705', 'phone': '(512) 458-8400', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True},
                {'name': 'Texas Orthopedics', 'address': '4700 Seton Center Pkwy #100, Austin, TX 78759', 'phone': '(512) 439-1000', 'specialty': 'Sports Medicine & PRP', 'priceRange': '$3,500 - $9,000', 'featured': True, 'verified': True}
            ]
        },
        'Fort Worth': {
            'avgPrice': 4600,
            'clinics': [
                {'name': 'Fort Worth Regenerative Medicine', 'address': '1325 Pennsylvania Ave #200, Fort Worth, TX 76104', 'phone': '(817) 336-4600', 'specialty': 'Stem Cell Therapy', 'priceRange': '$3,500 - $9,000', 'featured': True, 'verified': True},
                {'name': 'Texas Health Harris Methodist', 'address': '1301 Pennsylvania Ave, Fort Worth, TX 76104', 'phone': '(817) 250-2000', 'specialty': 'Orthopedic Regenerative Care', 'priceRange': '$4,500 - $12,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Florida': {
        'Jacksonville': {
            'avgPrice': 5000,
            'clinics': [
                {'name': 'Jacksonville Stem Cell Center', 'address': '4500 San Pablo Rd S, Jacksonville, FL 32224', 'phone': '(904) 953-2000', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True},
                {'name': 'First Coast Orthopedics', 'address': '836 Prudential Dr #1400, Jacksonville, FL 32207', 'phone': '(904) 398-5757', 'specialty': 'Orthopedic Stem Cell Therapy', 'priceRange': '$3,500 - $9,000', 'featured': False, 'verified': True}
            ]
        },
        'Miami': {
            'avgPrice': 6100,
            'clinics': [
                {'name': 'Miami Stem Cell Treatment Center', 'address': '1150 NW 14th St #300, Miami, FL 33136', 'phone': '(305) 243-4000', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$5,000 - $15,000', 'featured': True, 'verified': True},
                {'name': 'University of Miami Sports Medicine', 'address': '1400 NW 12th Ave, Miami, FL 33136', 'phone': '(305) 243-3000', 'specialty': 'Academic Sports Medicine', 'priceRange': '$6,000 - $18,000', 'featured': True, 'verified': True},
                {'name': 'South Florida Orthopedics', 'address': '8940 N Kendall Dr #903E, Miami, FL 33176', 'phone': '(305) 596-0044', 'specialty': 'Joint Regeneration', 'priceRange': '$4,500 - $12,000', 'featured': False, 'verified': True}
            ]
        },
        'Tampa': {
            'avgPrice': 5200,
            'clinics': [
                {'name': 'Tampa Bay Stem Cell Center', 'address': '2 Tampa General Cir, Tampa, FL 33606', 'phone': '(813) 844-7000', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,500 - $12,000', 'featured': True, 'verified': True},
                {'name': 'Florida Orthopedic Institute', 'address': '13020 N Telecom Pkwy, Temple Terrace, FL 33637', 'phone': '(813) 978-9700', 'specialty': 'Orthopedic Stem Cell Therapy', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True}
            ]
        },
        'Orlando': {
            'avgPrice': 5100,
            'clinics': [
                {'name': 'Orlando Stem Cell Treatment Center', 'address': '1222 S Orange Ave, Orlando, FL 32806', 'phone': '(407) 841-3720', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $11,000', 'featured': True, 'verified': True},
                {'name': 'Orlando Health Orthopedics', 'address': '1414 Kuhl Ave, Orlando, FL 32806', 'phone': '(321) 841-5111', 'specialty': 'Sports Medicine & PRP', 'priceRange': '$4,500 - $12,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Arizona': {
        'Phoenix': {
            'avgPrice': 5000,
            'clinics': [
                {'name': 'Phoenix Stem Cell Treatment Center', 'address': '9250 N 3rd St #1004, Phoenix, AZ 85020', 'phone': '(602) 633-4000', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True},
                {'name': 'Arizona Center for Regenerative Medicine', 'address': '8415 N Pima Rd #210, Scottsdale, AZ 85258', 'phone': '(480) 556-0019', 'specialty': 'Stem Cell Therapy', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True}
            ]
        },
        'Tucson': {
            'avgPrice': 4500,
            'clinics': [
                {'name': 'Tucson Regenerative Medicine', 'address': '1501 N Campbell Ave, Tucson, AZ 85724', 'phone': '(520) 626-6000', 'specialty': 'Orthopedic Regenerative Care', 'priceRange': '$3,500 - $9,000', 'featured': True, 'verified': True},
                {'name': 'Southern Arizona Orthopedics', 'address': '5301 E Grant Rd, Tucson, AZ 85712', 'phone': '(520) 784-6200', 'specialty': 'Sports Medicine & PRP', 'priceRange': '$4,000 - $10,000', 'featured': False, 'verified': True}
            ]
        },
        'Scottsdale': {
            'avgPrice': 5500,
            'clinics': [
                {'name': 'Scottsdale Stem Cell Treatment Center', 'address': '9377 E Bell Rd #333, Scottsdale, AZ 85260', 'phone': '(480) 860-2030', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True},
                {'name': 'Mayo Clinic Arizona', 'address': '5777 E Mayo Blvd, Phoenix, AZ 85054', 'phone': '(480) 515-6296', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$8,000 - $20,000', 'featured': True, 'verified': True},
                {'name': 'OrthoArizona', 'address': '2222 E Highland Ave #200, Phoenix, AZ 85016', 'phone': '(602) 263-8700', 'specialty': 'Orthopedic Stem Cell Therapy', 'priceRange': '$4,000 - $10,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Colorado': {
        'Denver': {
            'avgPrice': 5300,
            'clinics': [
                {'name': 'Denver Stem Cell Center', 'address': '799 E Hampden Ave #500, Englewood, CO 80113', 'phone': '(303) 788-8000', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,500 - $12,000', 'featured': True, 'verified': True},
                {'name': 'Colorado Center for Orthopedic Excellence', 'address': '2535 S Downing St #100, Denver, CO 80210', 'phone': '(303) 695-6060', 'specialty': 'Orthopedic Stem Cell Therapy', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True},
                {'name': 'Steadman Clinic', 'address': '181 W Meadow Dr #400, Vail, CO 81657', 'phone': '(970) 476-1100', 'specialty': 'Elite Sports Medicine', 'priceRange': '$8,000 - $25,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'New York': {
        'New York City': {
            'avgPrice': 6500,
            'clinics': [
                {'name': 'Hospital for Special Surgery', 'address': '535 E 70th St, New York, NY 10021', 'phone': '(212) 606-1000', 'specialty': 'Academic Orthopedic Excellence', 'priceRange': '$8,000 - $25,000', 'featured': True, 'verified': True},
                {'name': 'NYC Stem Cell Treatment Center', 'address': '635 Madison Ave #1400, New York, NY 10022', 'phone': '(212) 288-3056', 'specialty': 'Regenerative Medicine', 'priceRange': '$6,000 - $15,000', 'featured': True, 'verified': True},
                {'name': 'Manhattan Orthopedic Care', 'address': '121 E 60th St #1C, New York, NY 10022', 'phone': '(212) 310-0100', 'specialty': 'Sports Medicine & PRP', 'priceRange': '$5,000 - $12,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Georgia': {
        'Atlanta': {
            'avgPrice': 5100,
            'clinics': [
                {'name': 'Emory Orthopedics & Spine Center', 'address': '59 Executive Park S NE, Atlanta, GA 30329', 'phone': '(404) 778-3350', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $15,000', 'featured': True, 'verified': True},
                {'name': 'Atlanta Stem Cell Treatment Center', 'address': '5673 Peachtree Dunwoody Rd #850, Atlanta, GA 30342', 'phone': '(404) 255-0226', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Illinois': {
        'Chicago': {
            'avgPrice': 5600,
            'clinics': [
                {'name': 'Rush University Medical Center', 'address': '1611 W Harrison St, Chicago, IL 60612', 'phone': '(312) 942-5000', 'specialty': 'Academic Orthopedic Excellence', 'priceRange': '$6,000 - $18,000', 'featured': True, 'verified': True},
                {'name': 'Chicago Stem Cell Treatment Center', 'address': '680 N Lake Shore Dr #930, Chicago, IL 60611', 'phone': '(312) 337-7900', 'specialty': 'Regenerative Medicine', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True},
                {'name': 'Midwest Orthopedics at Rush', 'address': '1611 W Harrison St #300, Chicago, IL 60612', 'phone': '(877) 632-6637', 'specialty': 'Sports Medicine & PRP', 'priceRange': '$4,500 - $10,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Washington': {
        'Seattle': {
            'avgPrice': 5500,
            'clinics': [
                {'name': 'Seattle Stem Cell Center', 'address': '1959 NE Pacific St, Seattle, WA 98195', 'phone': '(206) 598-4288', 'specialty': 'Regenerative Medicine', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True},
                {'name': 'UW Medicine Orthopedics', 'address': '4245 Roosevelt Way NE, Seattle, WA 98105', 'phone': '(206) 520-5000', 'specialty': 'Academic Orthopedic Care', 'priceRange': '$5,500 - $15,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Massachusetts': {
        'Boston': {
            'avgPrice': 6200,
            'clinics': [
                {'name': 'Massachusetts General Hospital', 'address': '55 Fruit St, Boston, MA 02114', 'phone': '(617) 726-2000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$7,000 - $20,000', 'featured': True, 'verified': True},
                {'name': 'Boston Stem Cell Treatment Center', 'address': '800 Boylston St #1600, Boston, MA 02199', 'phone': '(617) 262-5200', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$5,500 - $14,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Nevada': {
        'Las Vegas': {
            'avgPrice': 4800,
            'clinics': [
                {'name': 'Las Vegas Stem Cell Treatment Center', 'address': '2020 Palomino Ln #100, Las Vegas, NV 89106', 'phone': '(702) 732-0282', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True},
                {'name': 'Nevada Orthopedic & Spine Center', 'address': '2800 E Desert Inn Rd #100, Las Vegas, NV 89121', 'phone': '(702) 258-3773', 'specialty': 'Orthopedic Stem Cell Therapy', 'priceRange': '$3,500 - $9,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Ohio': {
        'Columbus': {
            'avgPrice': 4800,
            'clinics': [
                {'name': 'Ohio State Wexner Medical Center', 'address': '410 W 10th Ave, Columbus, OH 43210', 'phone': '(614) 293-8000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True},
                {'name': 'Columbus Stem Cell Treatment Center', 'address': '300 E Town St #200, Columbus, OH 43215', 'phone': '(614) 221-6100', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': False, 'verified': True}
            ]
        },
        'Cleveland': {
            'avgPrice': 5200,
            'clinics': [
                {'name': 'Cleveland Clinic', 'address': '9500 Euclid Ave, Cleveland, OH 44195', 'phone': '(216) 444-2200', 'specialty': 'World-Class Orthopedic Care', 'priceRange': '$6,000 - $18,000', 'featured': True, 'verified': True},
                {'name': 'Cleveland Stem Cell Treatment Center', 'address': '25501 Chagrin Blvd #200, Beachwood, OH 44122', 'phone': '(216) 831-1000', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,500 - $11,000', 'featured': True, 'verified': True}
            ]
        },
        'Cincinnati': {
            'avgPrice': 4600,
            'clinics': [
                {'name': 'Cincinnati Stem Cell Treatment Center', 'address': '222 Piedmont Ave #8300, Cincinnati, OH 45219', 'phone': '(513) 584-1000', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Pennsylvania': {
        'Philadelphia': {
            'avgPrice': 5800,
            'clinics': [
                {'name': 'Penn Medicine', 'address': '3400 Spruce St, Philadelphia, PA 19104', 'phone': '(215) 662-4000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$6,000 - $18,000', 'featured': True, 'verified': True},
                {'name': 'Philadelphia Stem Cell Treatment Center', 'address': '1800 JFK Blvd #1500, Philadelphia, PA 19103', 'phone': '(215) 567-2020', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True}
            ]
        },
        'Pittsburgh': {
            'avgPrice': 5000,
            'clinics': [
                {'name': 'UPMC Sports Medicine', 'address': '3200 S Water St, Pittsburgh, PA 15203', 'phone': '(412) 432-3600', 'specialty': 'Elite Sports Medicine', 'priceRange': '$5,000 - $15,000', 'featured': True, 'verified': True},
                {'name': 'Pittsburgh Stem Cell Treatment Center', 'address': '5750 Centre Ave, Pittsburgh, PA 15206', 'phone': '(412) 661-2000', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,000 - $10,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Tennessee': {
        'Nashville': {
            'avgPrice': 4900,
            'clinics': [
                {'name': 'Vanderbilt Orthopedics', 'address': '1215 21st Ave S, Nashville, TN 37232', 'phone': '(615) 322-5000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True},
                {'name': 'Nashville Stem Cell Treatment Center', 'address': '2011 Church St #400, Nashville, TN 37203', 'phone': '(615) 329-1234', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True}
            ]
        },
        'Memphis': {
            'avgPrice': 4500,
            'clinics': [
                {'name': 'Campbell Clinic', 'address': '1400 S Germantown Rd, Germantown, TN 38138', 'phone': '(901) 759-3100', 'specialty': 'Historic Orthopedic Excellence', 'priceRange': '$4,500 - $12,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Michigan': {
        'Detroit': {
            'avgPrice': 4800,
            'clinics': [
                {'name': 'Henry Ford Health', 'address': '2799 W Grand Blvd, Detroit, MI 48202', 'phone': '(313) 916-2600', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True},
                {'name': 'Detroit Stem Cell Treatment Center', 'address': '26850 Providence Pkwy, Novi, MI 48374', 'phone': '(248) 465-4141', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Minnesota': {
        'Minneapolis': {
            'avgPrice': 5400,
            'clinics': [
                {'name': 'Mayo Clinic Rochester', 'address': '200 First St SW, Rochester, MN 55905', 'phone': '(507) 284-2511', 'specialty': 'World-Class Medical Care', 'priceRange': '$8,000 - $25,000', 'featured': True, 'verified': True},
                {'name': 'Minneapolis Stem Cell Treatment Center', 'address': '825 S 8th St #200, Minneapolis, MN 55404', 'phone': '(612) 338-2020', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,500 - $11,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Missouri': {
        'St. Louis': {
            'avgPrice': 4700,
            'clinics': [
                {'name': 'Washington University Orthopedics', 'address': '660 S Euclid Ave, St. Louis, MO 63110', 'phone': '(314) 747-2500', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True},
                {'name': 'St. Louis Stem Cell Treatment Center', 'address': '1034 S Brentwood Blvd #1500, St. Louis, MO 63117', 'phone': '(314) 726-2020', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': False, 'verified': True}
            ]
        },
        'Kansas City': {
            'avgPrice': 4500,
            'clinics': [
                {'name': 'Kansas City Stem Cell Treatment Center', 'address': '4320 Wornall Rd #200, Kansas City, MO 64111', 'phone': '(816) 531-0000', 'specialty': 'Regenerative Medicine', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'North Carolina': {
        'Charlotte': {
            'avgPrice': 4900,
            'clinics': [
                {'name': 'Atrium Health Orthopedics', 'address': '1000 Blythe Blvd, Charlotte, NC 28203', 'phone': '(704) 355-2000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True},
                {'name': 'Charlotte Stem Cell Treatment Center', 'address': '1915 Randolph Rd #200, Charlotte, NC 28207', 'phone': '(704) 333-4000', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True}
            ]
        },
        'Raleigh': {
            'avgPrice': 4700,
            'clinics': [
                {'name': 'Duke Orthopedics Raleigh', 'address': '3480 Wake Forest Rd #600, Raleigh, NC 27609', 'phone': '(919) 403-5000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Oregon': {
        'Portland': {
            'avgPrice': 5200,
            'clinics': [
                {'name': 'OHSU Orthopedics', 'address': '3181 SW Sam Jackson Park Rd, Portland, OR 97239', 'phone': '(503) 494-8311', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True},
                {'name': 'Portland Stem Cell Treatment Center', 'address': '9155 SW Barnes Rd #930, Portland, OR 97225', 'phone': '(503) 297-8081', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,500 - $11,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Maryland': {
        'Baltimore': {
            'avgPrice': 5500,
            'clinics': [
                {'name': 'Johns Hopkins Orthopedics', 'address': '601 N Caroline St, Baltimore, MD 21287', 'phone': '(410) 955-5000', 'specialty': 'World-Class Academic Medicine', 'priceRange': '$7,000 - $20,000', 'featured': True, 'verified': True},
                {'name': 'Baltimore Stem Cell Treatment Center', 'address': '100 E Pratt St #2500, Baltimore, MD 21202', 'phone': '(410) 332-9000', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Indiana': {
        'Indianapolis': {
            'avgPrice': 4600,
            'clinics': [
                {'name': 'IU Health Orthopedics', 'address': '1801 N Senate Blvd, Indianapolis, IN 46202', 'phone': '(317) 962-2000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True},
                {'name': 'Indianapolis Stem Cell Treatment Center', 'address': '8402 Harcourt Rd #100, Indianapolis, IN 46260', 'phone': '(317) 872-2020', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': False, 'verified': True}
            ]
        }
    },
    'Utah': {
        'Salt Lake City': {
            'avgPrice': 4800,
            'clinics': [
                {'name': 'University of Utah Orthopedics', 'address': '590 Wakara Way, Salt Lake City, UT 84108', 'phone': '(801) 587-7000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True},
                {'name': 'Salt Lake Stem Cell Treatment Center', 'address': '50 N Medical Dr, Salt Lake City, UT 84132', 'phone': '(801) 581-2121', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$4,000 - $10,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Kentucky': {
        'Louisville': {
            'avgPrice': 4400,
            'clinics': [
                {'name': 'UofL Health Orthopedics', 'address': '530 S Jackson St, Louisville, KY 40202', 'phone': '(502) 588-4000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$4,500 - $12,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Oklahoma': {
        'Oklahoma City': {
            'avgPrice': 4300,
            'clinics': [
                {'name': 'OU Health Orthopedics', 'address': '700 NE 13th St, Oklahoma City, OK 73104', 'phone': '(405) 271-4000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$4,000 - $11,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Wisconsin': {
        'Milwaukee': {
            'avgPrice': 4700,
            'clinics': [
                {'name': 'Froedtert Orthopedics', 'address': '9200 W Wisconsin Ave, Milwaukee, WI 53226', 'phone': '(414) 805-3000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'New Mexico': {
        'Albuquerque': {
            'avgPrice': 4400,
            'clinics': [
                {'name': 'UNM Health Orthopedics', 'address': '2211 Lomas Blvd NE, Albuquerque, NM 87106', 'phone': '(505) 272-2111', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$4,000 - $11,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Hawaii': {
        'Honolulu': {
            'avgPrice': 5800,
            'clinics': [
                {'name': 'Hawaii Pacific Health Orthopedics', 'address': '1380 Lusitana St, Honolulu, HI 96813', 'phone': '(808) 535-7000', 'specialty': 'Island Regenerative Medicine', 'priceRange': '$5,500 - $15,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Alaska': {
        'Anchorage': {
            'avgPrice': 5500,
            'clinics': [
                {'name': 'Alaska Regional Orthopedics', 'address': '2801 Debarr Rd, Anchorage, AK 99508', 'phone': '(907) 264-1754', 'specialty': 'Northern Regenerative Medicine', 'priceRange': '$5,000 - $14,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Idaho': {
        'Boise': {
            'avgPrice': 4500,
            'clinics': [
                {'name': 'St. Luke\'s Orthopedics', 'address': '190 E Bannock St, Boise, ID 83712', 'phone': '(208) 381-2222', 'specialty': 'Regional Regenerative Medicine', 'priceRange': '$4,000 - $11,000', 'featured': True, 'verified': True}
            ]
        }
    },
    'Washington DC': {
        'Washington': {
            'avgPrice': 6000,
            'clinics': [
                {'name': 'Georgetown University Hospital', 'address': '3800 Reservoir Rd NW, Washington, DC 20007', 'phone': '(202) 444-2000', 'specialty': 'Academic Regenerative Medicine', 'priceRange': '$6,000 - $18,000', 'featured': True, 'verified': True},
                {'name': 'Washington DC Stem Cell Center', 'address': '1145 19th St NW #800, Washington, DC 20036', 'phone': '(202) 223-2020', 'specialty': 'Regenerative Orthopedics', 'priceRange': '$5,000 - $12,000', 'featured': True, 'verified': True}
            ]
        }
    }
}

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def get_state_image(state):
    """Get the image path for a state"""
    return f'/assets/images/states/{slugify(state)}.jpg'

def get_city_image(city):
    """Get the image path for a city"""
    return f'/assets/images/cities/{slugify(city)}.jpg'

def generate_html_header(title, description, canonical_url):
    """Generate HTML header with SEO meta tags"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | OrthoFinder - Stem Cell Therapy Directory</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="https://stem-cells-dir.netlify.app{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <style>
        .hero-gradient {{ background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 58, 138, 0.8) 100%); }}
        .card-hover {{ transition: all 0.3s ease; }}
        .card-hover:hover {{ transform: translateY(-4px); box-shadow: 0 20px 40px rgba(0,0,0,0.15); }}
    </style>
</head>
<body class="bg-slate-50">
'''

def generate_nav():
    """Generate navigation bar"""
    return '''
    <nav class="bg-white/95 backdrop-blur-md shadow-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <a href="/" class="text-xl font-bold text-blue-900">OrthoFinder<span class="text-blue-500">.</span></a>
                </div>
                <div class="hidden md:flex items-center space-x-8">
                    <a href="/" class="text-slate-600 hover:text-blue-600">Home</a>
                    <a href="/#cost-guide" class="text-slate-600 hover:text-blue-600">Cost Guide</a>
                    <a href="/locations/" class="text-slate-600 hover:text-blue-600">All Locations</a>
                    <a href="/#mexico" class="text-slate-600 hover:text-blue-600">Mexico Clinics</a>
                </div>
            </div>
        </div>
    </nav>
'''

def generate_footer():
    """Generate footer"""
    return '''
    <footer class="bg-slate-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div>
                    <h3 class="text-xl font-bold mb-4">OrthoFinder<span class="text-blue-400">.</span></h3>
                    <p class="text-slate-400 text-sm">Your trusted resource for stem cell therapy pricing and clinic information.</p>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Cost Guides</h4>
                    <ul class="space-y-2 text-sm text-slate-400">
                        <li><a href="/#cost-guide" class="hover:text-white">Knee Stem Cell Cost</a></li>
                        <li><a href="/#cost-guide" class="hover:text-white">Back & Spine Cost</a></li>
                        <li><a href="/#cost-guide" class="hover:text-white">Shoulder Cost</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Popular States</h4>
                    <ul class="space-y-2 text-sm text-slate-400">
                        <li><a href="/locations/california/" class="hover:text-white">California</a></li>
                        <li><a href="/locations/texas/" class="hover:text-white">Texas</a></li>
                        <li><a href="/locations/florida/" class="hover:text-white">Florida</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Legal</h4>
                    <ul class="space-y-2 text-sm text-slate-400">
                        <li><a href="/#" class="hover:text-white">Privacy Policy</a></li>
                        <li><a href="/#" class="hover:text-white">Terms of Service</a></li>
                        <li><a href="/#" class="hover:text-white">Medical Disclaimer</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-slate-800 mt-8 pt-8 text-center text-sm text-slate-500">
                <p>&copy; 2025 OrthoFinder. All rights reserved. Not medical advice.</p>
            </div>
        </div>
    </footer>
</body>
</html>
'''

def generate_state_page(state, cities_data):
    """Generate a state directory page"""
    state_slug = slugify(state)
    state_image = get_state_image(state)
    
    total_clinics = sum(len(city_data['clinics']) for city_data in cities_data.values())
    avg_price = sum(city_data['avgPrice'] for city_data in cities_data.values()) // len(cities_data)
    
    title = f"Stem Cell Clinics in {state}"
    description = f"Find {total_clinics}+ verified stem cell therapy clinics in {state}. Compare prices, read reviews, and find the best regenerative medicine providers near you."
    canonical = f"/locations/{state_slug}/"
    
    html = generate_html_header(title, description, canonical)
    html += generate_nav()
    
    # Hero section with state image
    html += f'''
    <div class="relative h-80 bg-cover bg-center" style="background-image: url('{state_image}');">
        <div class="absolute inset-0 hero-gradient"></div>
        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex flex-col justify-center">
            <nav class="text-sm text-blue-200 mb-4">
                <a href="/" class="hover:text-white">Home</a>
                <span class="mx-2">/</span>
                <a href="/locations/" class="hover:text-white">Locations</a>
                <span class="mx-2">/</span>
                <span class="text-white">{state}</span>
            </nav>
            <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">Stem Cell Clinics in {state}</h1>
            <p class="text-xl text-blue-100">{total_clinics} Verified Clinics · {len(cities_data)} Cities · Avg. ${avg_price:,}</p>
        </div>
    </div>
    '''
    
    # Cities grid
    html += '''
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 class="text-2xl font-bold text-slate-900 mb-8">Cities in ''' + state + '''</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    '''
    
    for city, city_data in cities_data.items():
        city_slug = slugify(city)
        city_image = get_city_image(city)
        clinic_count = len(city_data['clinics'])
        
        html += f'''
            <a href="/locations/{state_slug}/{city_slug}/" class="card-hover bg-white rounded-xl overflow-hidden shadow-md">
                <div class="h-40 bg-cover bg-center" style="background-image: url('{city_image}');"></div>
                <div class="p-6">
                    <h3 class="text-xl font-bold text-slate-900 mb-2">{city}</h3>
                    <div class="flex justify-between text-sm text-slate-600">
                        <span>{clinic_count} Clinics</span>
                        <span>Avg. ${city_data['avgPrice']:,}</span>
                    </div>
                </div>
            </a>
        '''
    
    html += '''
        </div>
    </div>
    '''
    
    # Medical disclaimer
    html += '''
    <div class="bg-amber-50 border-l-4 border-amber-400 p-4 mx-4 md:mx-auto max-w-4xl mb-12">
        <div class="flex">
            <div class="ml-3">
                <p class="text-sm text-amber-700">
                    <strong>Medical Disclaimer:</strong> The information provided is for educational purposes only and is not intended as medical advice. 
                    Stem cell therapy is not FDA-approved for most orthopedic conditions. Always consult with a qualified healthcare provider.
                </p>
            </div>
        </div>
    </div>
    '''
    
    html += generate_footer()
    return html

def generate_city_page(state, city, city_data):
    """Generate a city directory page with clinic listings"""
    state_slug = slugify(state)
    city_slug = slugify(city)
    city_image = get_city_image(city)
    
    clinics = city_data['clinics']
    avg_price = city_data['avgPrice']
    
    title = f"Stem Cell Clinics in {city}, {state}"
    description = f"Find {len(clinics)} verified stem cell therapy clinics in {city}, {state}. Average cost ${avg_price:,}. Compare prices and find the best regenerative medicine providers."
    canonical = f"/locations/{state_slug}/{city_slug}/"
    
    html = generate_html_header(title, description, canonical)
    html += generate_nav()
    
    # Hero section with city image
    html += f'''
    <div class="relative h-80 bg-cover bg-center" style="background-image: url('{city_image}');">
        <div class="absolute inset-0 hero-gradient"></div>
        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex flex-col justify-center">
            <nav class="text-sm text-blue-200 mb-4">
                <a href="/" class="hover:text-white">Home</a>
                <span class="mx-2">/</span>
                <a href="/locations/" class="hover:text-white">Locations</a>
                <span class="mx-2">/</span>
                <a href="/locations/{state_slug}/" class="hover:text-white">{state}</a>
                <span class="mx-2">/</span>
                <span class="text-white">{city}</span>
            </nav>
            <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">Stem Cell Clinics in {city}</h1>
            <p class="text-xl text-blue-100">{len(clinics)} Verified Clinics · Average ${avg_price:,}</p>
        </div>
    </div>
    '''
    
    # Clinics list
    html += '''
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 class="text-2xl font-bold text-slate-900 mb-8">Verified Stem Cell Clinics</h2>
        <div class="space-y-6">
    '''
    
    for clinic in clinics:
        clinic_slug = slugify(clinic['name'])
        featured_badge = '<span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">Featured</span>' if clinic.get('featured') else ''
        verified_badge = '<span class="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">Verified</span>' if clinic.get('verified') else ''
        
        html += f'''
            <div class="card-hover bg-white rounded-xl shadow-md p-6">
                <div class="flex flex-col md:flex-row md:items-center md:justify-between">
                    <div class="flex-1">
                        <div class="flex items-center gap-2 mb-2">
                            <h3 class="text-xl font-bold text-slate-900">{clinic['name']}</h3>
                            {featured_badge}
                            {verified_badge}
                        </div>
                        <p class="text-slate-600 mb-2">{clinic['address']}</p>
                        <p class="text-slate-500 text-sm mb-2">{clinic['specialty']}</p>
                        <p class="text-blue-600 font-medium">{clinic['phone']}</p>
                    </div>
                    <div class="mt-4 md:mt-0 md:ml-6 text-right">
                        <p class="text-2xl font-bold text-slate-900">{clinic['priceRange']}</p>
                        <p class="text-sm text-slate-500">Estimated Range</p>
                        <a href="/locations/{state_slug}/{city_slug}/{clinic_slug}.html" class="mt-4 inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition">
                            View Details
                        </a>
                    </div>
                </div>
            </div>
        '''
    
    html += '''
        </div>
    </div>
    '''
    
    # Medical disclaimer
    html += '''
    <div class="bg-amber-50 border-l-4 border-amber-400 p-4 mx-4 md:mx-auto max-w-4xl mb-12">
        <div class="flex">
            <div class="ml-3">
                <p class="text-sm text-amber-700">
                    <strong>Medical Disclaimer:</strong> The information provided is for educational purposes only and is not intended as medical advice. 
                    Stem cell therapy is not FDA-approved for most orthopedic conditions. Always consult with a qualified healthcare provider.
                </p>
            </div>
        </div>
    </div>
    '''
    
    html += generate_footer()
    return html

def generate_clinic_page(state, city, clinic, city_data):
    """Generate an individual clinic detail page"""
    state_slug = slugify(state)
    city_slug = slugify(city)
    clinic_slug = slugify(clinic['name'])
    city_image = get_city_image(city)
    
    title = f"{clinic['name']} - Stem Cell Therapy in {city}, {state}"
    description = f"{clinic['name']} offers {clinic['specialty']} in {city}, {state}. Price range: {clinic['priceRange']}. Contact: {clinic['phone']}"
    canonical = f"/locations/{state_slug}/{city_slug}/{clinic_slug}.html"
    
    html = generate_html_header(title, description, canonical)
    html += generate_nav()
    
    # Hero section
    html += f'''
    <div class="relative h-64 bg-cover bg-center" style="background-image: url('{city_image}');">
        <div class="absolute inset-0 hero-gradient"></div>
        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex flex-col justify-center">
            <nav class="text-sm text-blue-200 mb-4">
                <a href="/" class="hover:text-white">Home</a>
                <span class="mx-2">/</span>
                <a href="/locations/" class="hover:text-white">Locations</a>
                <span class="mx-2">/</span>
                <a href="/locations/{state_slug}/" class="hover:text-white">{state}</a>
                <span class="mx-2">/</span>
                <a href="/locations/{state_slug}/{city_slug}/" class="hover:text-white">{city}</a>
                <span class="mx-2">/</span>
                <span class="text-white">{clinic['name']}</span>
            </nav>
            <h1 class="text-3xl md:text-4xl font-bold text-white">{clinic['name']}</h1>
        </div>
    </div>
    '''
    
    featured_badge = '<span class="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded">Featured Clinic</span>' if clinic.get('featured') else ''
    verified_badge = '<span class="bg-green-100 text-green-800 text-sm font-medium px-3 py-1 rounded">Verified Provider</span>' if clinic.get('verified') else ''
    
    # Clinic details
    html += f'''
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2">
                <div class="bg-white rounded-xl shadow-md p-8">
                    <div class="flex items-center gap-3 mb-6">
                        {featured_badge}
                        {verified_badge}
                    </div>
                    
                    <h2 class="text-2xl font-bold text-slate-900 mb-4">About This Clinic</h2>
                    <p class="text-slate-600 mb-6">
                        {clinic['name']} is a {clinic['specialty'].lower()} provider located in {city}, {state}. 
                        They offer stem cell therapy and regenerative medicine treatments for various orthopedic conditions 
                        including knee osteoarthritis, spine and disc issues, shoulder injuries, and hip problems.
                    </p>
                    
                    <h3 class="text-xl font-bold text-slate-900 mb-3">Specialty</h3>
                    <p class="text-slate-600 mb-6">{clinic['specialty']}</p>
                    
                    <h3 class="text-xl font-bold text-slate-900 mb-3">Treatments Offered</h3>
                    <ul class="list-disc list-inside text-slate-600 mb-6 space-y-2">
                        <li>PRP (Platelet-Rich Plasma) Therapy</li>
                        <li>Bone Marrow Aspirate Concentrate (BMAC)</li>
                        <li>Adipose-Derived Stem Cell Therapy</li>
                        <li>Regenerative Joint Injections</li>
                    </ul>
                    
                    <h3 class="text-xl font-bold text-slate-900 mb-3">Conditions Treated</h3>
                    <ul class="list-disc list-inside text-slate-600 space-y-2">
                        <li>Knee Osteoarthritis</li>
                        <li>Spine & Disc Degeneration</li>
                        <li>Shoulder Injuries (Rotator Cuff)</li>
                        <li>Hip Osteoarthritis</li>
                        <li>Sports Injuries</li>
                    </ul>
                </div>
            </div>
            
            <div class="lg:col-span-1">
                <div class="bg-white rounded-xl shadow-md p-6 sticky top-24">
                    <h3 class="text-xl font-bold text-slate-900 mb-4">Contact Information</h3>
                    
                    <div class="space-y-4">
                        <div>
                            <p class="text-sm text-slate-500">Address</p>
                            <p class="text-slate-900">{clinic['address']}</p>
                        </div>
                        
                        <div>
                            <p class="text-sm text-slate-500">Phone</p>
                            <p class="text-blue-600 font-medium">{clinic['phone']}</p>
                        </div>
                        
                        <div>
                            <p class="text-sm text-slate-500">Price Range</p>
                            <p class="text-2xl font-bold text-slate-900">{clinic['priceRange']}</p>
                        </div>
                        
                        <a href="tel:{clinic['phone'].replace('(', '').replace(')', '').replace(' ', '').replace('-', '')}" 
                           class="block w-full bg-blue-600 text-white text-center px-6 py-3 rounded-lg hover:bg-blue-700 transition">
                            Call Now
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    # Other clinics in this city
    other_clinics = [c for c in city_data['clinics'] if c['name'] != clinic['name']]
    if other_clinics:
        html += f'''
        <div class="bg-slate-100 py-12">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <h2 class="text-2xl font-bold text-slate-900 mb-6">Other Clinics in {city}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        '''
        
        for other in other_clinics[:4]:
            other_slug = slugify(other['name'])
            html += f'''
                    <a href="/locations/{state_slug}/{city_slug}/{other_slug}.html" class="card-hover bg-white rounded-xl shadow-md p-6">
                        <h3 class="text-lg font-bold text-slate-900 mb-2">{other['name']}</h3>
                        <p class="text-slate-600 text-sm mb-2">{other['specialty']}</p>
                        <p class="text-blue-600 font-medium">{other['priceRange']}</p>
                    </a>
            '''
        
        html += '''
                </div>
            </div>
        </div>
        '''
    
    # Medical disclaimer
    html += '''
    <div class="bg-amber-50 border-l-4 border-amber-400 p-4 mx-4 md:mx-auto max-w-4xl my-12">
        <div class="flex">
            <div class="ml-3">
                <p class="text-sm text-amber-700">
                    <strong>Medical Disclaimer:</strong> The information provided is for educational purposes only and is not intended as medical advice. 
                    Stem cell therapy is not FDA-approved for most orthopedic conditions. Always consult with a qualified healthcare provider before 
                    undergoing any medical treatment. Pricing is estimated and may vary.
                </p>
            </div>
        </div>
    </div>
    '''
    
    html += generate_footer()
    return html

def generate_all_states_page():
    """Generate the main locations index page"""
    title = "All Stem Cell Clinic Locations"
    description = "Browse stem cell therapy clinics across all 50 US states. Find verified providers, compare prices, and locate the best regenerative medicine clinics near you."
    canonical = "/locations/"
    
    html = generate_html_header(title, description, canonical)
    html += generate_nav()
    
    # Hero section
    html += '''
    <div class="relative h-64 bg-gradient-to-r from-blue-900 to-blue-700">
        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex flex-col justify-center">
            <nav class="text-sm text-blue-200 mb-4">
                <a href="/" class="hover:text-white">Home</a>
                <span class="mx-2">/</span>
                <span class="text-white">All Locations</span>
            </nav>
            <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">Stem Cell Clinic Directory</h1>
            <p class="text-xl text-blue-100">Browse clinics across all US states</p>
        </div>
    </div>
    '''
    
    # States grid
    html += '''
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    '''
    
    for state, cities_data in sorted(CLINIC_DATABASE.items()):
        state_slug = slugify(state)
        state_image = get_state_image(state)
        total_clinics = sum(len(city_data['clinics']) for city_data in cities_data.values())
        
        html += f'''
            <a href="/locations/{state_slug}/" class="card-hover bg-white rounded-xl overflow-hidden shadow-md">
                <div class="h-32 bg-cover bg-center" style="background-image: url('{state_image}');"></div>
                <div class="p-4">
                    <h3 class="text-lg font-bold text-slate-900">{state}</h3>
                    <p class="text-sm text-slate-600">{total_clinics} Clinics · {len(cities_data)} Cities</p>
                </div>
            </a>
        '''
    
    html += '''
        </div>
    </div>
    '''
    
    html += generate_footer()
    return html

def main():
    """Generate all static pages"""
    base_path = '/home/ubuntu/stem-cells/locations'
    
    # Generate main locations index
    print("Generating locations index page...")
    index_html = generate_all_states_page()
    with open(os.path.join(base_path, 'index.html'), 'w') as f:
        f.write(index_html)
    
    # Generate state and city pages
    for state, cities_data in CLINIC_DATABASE.items():
        state_slug = slugify(state)
        state_path = os.path.join(base_path, state_slug)
        os.makedirs(state_path, exist_ok=True)
        
        print(f"Generating {state} pages...")
        
        # State index page
        state_html = generate_state_page(state, cities_data)
        with open(os.path.join(state_path, 'index.html'), 'w') as f:
            f.write(state_html)
        
        # City pages
        for city, city_data in cities_data.items():
            city_slug = slugify(city)
            city_path = os.path.join(state_path, city_slug)
            os.makedirs(city_path, exist_ok=True)
            
            # City index page
            city_html = generate_city_page(state, city, city_data)
            with open(os.path.join(city_path, 'index.html'), 'w') as f:
                f.write(city_html)
            
            # Individual clinic pages
            for clinic in city_data['clinics']:
                clinic_slug = slugify(clinic['name'])
                clinic_html = generate_clinic_page(state, city, clinic, city_data)
                with open(os.path.join(city_path, f'{clinic_slug}.html'), 'w') as f:
                    f.write(clinic_html)
    
    print("Done! All pages generated.")

if __name__ == '__main__':
    main()
