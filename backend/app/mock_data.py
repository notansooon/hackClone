"""
Mock Product Database for PinkVanity Demo.

This contains the "Golden Examples" and additional demo data for hackathon presentation.
In production, this would be replaced by Supabase queries.
"""

# =============================================================================
# PERSONAL CARE PRODUCTS - Pink Tax Examples
# =============================================================================

WOMENS_PRODUCTS = {
    # Razors
    "gillette venus": {
        "id": "w001",
        "title": "Gillette Venus Original Razor",
        "price": 15.99,
        "category": "personal_care",
        "subcategory": "razors",
        "brand": "Gillette",
        "ingredients": [
            "5 blade cartridge",
            "moisture strip with aloe",
            "ergonomic handle",
            "pivoting head",
            "lubricating strip"
        ],
        "attributes": {
            "blade_count": 5,
            "has_moisture_strip": True,
            "pivoting_head": True
        },
        "retailers": ["target", "walmart", "cvs", "walgreens"],
        "image_url": "https://example.com/venus.jpg"
    },
    "schick intuition": {
        "id": "w002",
        "title": "Schick Intuition Sensitive Care Razor",
        "price": 12.49,
        "category": "personal_care",
        "subcategory": "razors",
        "brand": "Schick",
        "ingredients": [
            "4 blade cartridge",
            "skin conditioning solid",
            "aloe vera",
            "vitamin E",
            "pivoting head"
        ],
        "attributes": {
            "blade_count": 4,
            "has_moisture_strip": True,
            "pivoting_head": True
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/intuition.jpg"
    },

    # Shave Gel/Cream
    "skintimate raspberry": {
        "id": "w003",
        "title": "Skintimate Raspberry Rain Shave Gel",
        "price": 3.99,
        "category": "personal_care",
        "subcategory": "shave_gel",
        "brand": "Skintimate",
        "ingredients": [
            "water",
            "palmitic acid",
            "triethanolamine",
            "glycerin",
            "aloe barbadensis leaf juice",
            "fragrance",
            "vitamin E"
        ],
        "attributes": {
            "size_oz": 7,
            "skin_type": "sensitive",
            "scented": True
        },
        "retailers": ["target", "walmart", "cvs", "walgreens"],
        "image_url": "https://example.com/skintimate.jpg"
    },
    "eos shave cream": {
        "id": "w004",
        "title": "EOS Shea Better Shave Cream - Pomegranate Raspberry",
        "price": 4.79,
        "category": "personal_care",
        "subcategory": "shave_gel",
        "brand": "EOS",
        "ingredients": [
            "water",
            "glycerin",
            "shea butter",
            "aloe vera",
            "vitamin E",
            "jojoba oil",
            "fragrance"
        ],
        "attributes": {
            "size_oz": 7,
            "skin_type": "all",
            "scented": True
        },
        "retailers": ["target", "ulta", "cvs"],
        "image_url": "https://example.com/eos.jpg"
    },

    # Deodorant
    "secret invisible": {
        "id": "w005",
        "title": "Secret Invisible Solid Antiperspirant - Powder Fresh",
        "price": 6.49,
        "category": "personal_care",
        "subcategory": "deodorant",
        "brand": "Secret",
        "ingredients": [
            "aluminum zirconium tetrachlorohydrex gly",
            "cyclopentasiloxane",
            "stearyl alcohol",
            "ppg-14 butyl ether",
            "fragrance"
        ],
        "attributes": {
            "size_oz": 2.6,
            "type": "antiperspirant",
            "protection_hours": 48
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/secret.jpg"
    },

    # Body Wash
    "dove pink": {
        "id": "w006",
        "title": "Dove Pink Beauty Bar Soap",
        "price": 7.99,
        "category": "personal_care",
        "subcategory": "body_wash",
        "brand": "Dove",
        "ingredients": [
            "sodium lauroyl isethionate",
            "stearic acid",
            "sodium tallowate",
            "water",
            "sodium isethionate",
            "coconut acid",
            "fragrance"
        ],
        "attributes": {
            "count": 6,
            "moisturizing": True,
            "bar_size_oz": 3.75
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/dove-pink.jpg"
    },

    # Additional Products for Target Demo
    "nivea womens shave balm": {
        "id": "w007",
        "title": "Nivea Smooth Skin Shave Balm for Women",
        "price": 8.97,
        "category": "personal_care",
        "subcategory": "shave_care",
        "brand": "Nivea",
        "ingredients": [
            "water",
            "glycerin",
            "alcohol denat",
            "isopropyl palmitate",
            "chamomile extract",
            "vitamin E",
            "pink floral fragrance"
        ],
        "attributes": {
            "size_oz": 3.3,
            "skin_type": "sensitive",
            "alcohol_free": False
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/nivea-womens-balm.jpg"
    },

    "billie razor": {
        "id": "w008",
        "title": "Billie Women's 5-Blade Razor Starter Kit",
        "price": 12.99,
        "category": "personal_care",
        "subcategory": "razors",
        "brand": "Billie",
        "ingredients": [
            "5 sharp blades",
            "charcoal shave soap",
            "rounded edge",
            "magnetic holder",
            "encased in aloe"
        ],
        "attributes": {
            "blade_count": 5,
            "has_moisture_strip": True,
            "pivoting_head": True
        },
        "retailers": ["target", "walmart"],
        "image_url": "https://example.com/billie.jpg"
    },

    "degree women deodorant": {
        "id": "w009",
        "title": "Degree Women UltraClear Antiperspirant - Pure Rain",
        "price": 6.99,
        "category": "personal_care",
        "subcategory": "deodorant",
        "brand": "Degree",
        "ingredients": [
            "aluminum zirconium tetrachlorohydrex gly",
            "cyclopentasiloxane",
            "stearyl alcohol",
            "c12-15 alkyl benzoate",
            "fragrance"
        ],
        "attributes": {
            "size_oz": 2.6,
            "type": "antiperspirant",
            "protection_hours": 48
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/degree-women.jpg"
    },

    # Lotion - Classic Pink Tax Example
    "olay body lotion": {
        "id": "w010",
        "title": "Olay Quench Body Lotion - Shimmer",
        "price": 9.47,
        "category": "personal_care",
        "subcategory": "lotion",
        "brand": "Olay",
        "ingredients": [
            "water",
            "glycerin",
            "petrolatum",
            "isopropyl isostearate",
            "dimethicone",
            "niacinamide",
            "fragrance"
        ],
        "attributes": {
            "size_oz": 20.2,
            "moisturizing": True,
            "spf": False
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/olay-women.jpg"
    }
}

MENS_PRODUCTS = {
    # Razors - Men's Equivalents
    "gillette mach3": {
        "id": "m001",
        "title": "Gillette Mach3 Razor",
        "price": 9.99,
        "category": "personal_care",
        "subcategory": "razors",
        "brand": "Gillette",
        "ingredients": [
            "3 blade cartridge",
            "lubrication strip with aloe",
            "ergonomic handle",
            "pivoting head",
            "comfort guard"
        ],
        "attributes": {
            "blade_count": 3,
            "has_moisture_strip": True,
            "pivoting_head": True
        },
        "retailers": ["target", "walmart", "cvs", "walgreens"],
        "image_url": "https://example.com/mach3.jpg",
        "matches_womens": ["w001", "w002"]
    },
    "gillette fusion5": {
        "id": "m002",
        "title": "Gillette Fusion5 ProGlide Razor",
        "price": 11.99,
        "category": "personal_care",
        "subcategory": "razors",
        "brand": "Gillette",
        "ingredients": [
            "5 blade cartridge",
            "lubrication strip with aloe",
            "precision trimmer",
            "flexball handle",
            "pivoting head"
        ],
        "attributes": {
            "blade_count": 5,
            "has_moisture_strip": True,
            "pivoting_head": True
        },
        "retailers": ["target", "walmart", "cvs", "walgreens"],
        "image_url": "https://example.com/fusion5.jpg",
        "matches_womens": ["w001"]
    },

    # Shave Gel - Men's Equivalents
    "barbasol aloe": {
        "id": "m003",
        "title": "Barbasol Soothing Aloe Shave Cream",
        "price": 1.99,
        "category": "personal_care",
        "subcategory": "shave_gel",
        "brand": "Barbasol",
        "ingredients": [
            "water",
            "palmitic acid",
            "triethanolamine",
            "glycerin",
            "aloe barbadensis leaf juice",
            "lanolin",
            "fragrance"
        ],
        "attributes": {
            "size_oz": 10,
            "skin_type": "sensitive",
            "scented": True
        },
        "retailers": ["target", "walmart", "cvs", "walgreens"],
        "image_url": "https://example.com/barbasol.jpg",
        "matches_womens": ["w003", "w004"]
    },
    "gillette foamy": {
        "id": "m004",
        "title": "Gillette Foamy Sensitive Shave Foam",
        "price": 2.49,
        "category": "personal_care",
        "subcategory": "shave_gel",
        "brand": "Gillette",
        "ingredients": [
            "water",
            "palmitic acid",
            "triethanolamine",
            "glycerin",
            "aloe vera",
            "vitamin E"
        ],
        "attributes": {
            "size_oz": 11,
            "skin_type": "sensitive",
            "scented": False
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/foamy.jpg",
        "matches_womens": ["w003", "w004"]
    },

    # Deodorant - Men's Equivalent
    "old spice": {
        "id": "m005",
        "title": "Old Spice High Endurance Antiperspirant - Pure Sport",
        "price": 4.99,
        "category": "personal_care",
        "subcategory": "deodorant",
        "brand": "Old Spice",
        "ingredients": [
            "aluminum zirconium tetrachlorohydrex gly",
            "cyclopentasiloxane",
            "stearyl alcohol",
            "ppg-14 butyl ether",
            "fragrance"
        ],
        "attributes": {
            "size_oz": 3.0,
            "type": "antiperspirant",
            "protection_hours": 48
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/oldspice.jpg",
        "matches_womens": ["w005"]
    },

    # Body Wash - Men's Equivalent
    "dove men care": {
        "id": "m006",
        "title": "Dove Men+Care Body Bar Soap",
        "price": 6.99,
        "category": "personal_care",
        "subcategory": "body_wash",
        "brand": "Dove",
        "ingredients": [
            "sodium lauroyl isethionate",
            "stearic acid",
            "sodium tallowate",
            "water",
            "sodium isethionate",
            "coconut acid",
            "fragrance"
        ],
        "attributes": {
            "count": 6,
            "moisturizing": True,
            "bar_size_oz": 3.75
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/dove-men.jpg",
        "matches_womens": ["w006"]
    },

    # Additional Products for Target/Walmart Demo
    "nivea men shave balm": {
        "id": "m007",
        "title": "Nivea Men Sensitive Post Shave Balm",
        "price": 6.47,
        "category": "personal_care",
        "subcategory": "shave_care",
        "brand": "Nivea",
        "ingredients": [
            "water",
            "glycerin",
            "alcohol denat",
            "isopropyl palmitate",
            "chamomile extract",
            "vitamin E"
        ],
        "attributes": {
            "size_oz": 3.3,
            "skin_type": "sensitive",
            "alcohol_free": False
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/nivea-men-balm.jpg",
        "matches_womens": ["w007"]
    },

    "harry's razor": {
        "id": "m008",
        "title": "Harry's 5-Blade Razor with Handle",
        "price": 8.99,
        "category": "personal_care",
        "subcategory": "razors",
        "brand": "Harry's",
        "ingredients": [
            "5 german-engineered blades",
            "flex hinge",
            "lubricating strip",
            "rubber grip handle",
            "precision trimmer"
        ],
        "attributes": {
            "blade_count": 5,
            "has_moisture_strip": True,
            "pivoting_head": True
        },
        "retailers": ["target", "walmart"],
        "image_url": "https://example.com/harrys.jpg",
        "matches_womens": ["w001", "w002", "w008"]
    },

    "degree men deodorant": {
        "id": "m009",
        "title": "Degree Men UltraClear Antiperspirant",
        "price": 5.49,
        "category": "personal_care",
        "subcategory": "deodorant",
        "brand": "Degree",
        "ingredients": [
            "aluminum zirconium tetrachlorohydrex gly",
            "cyclopentasiloxane",
            "stearyl alcohol",
            "c12-15 alkyl benzoate",
            "fragrance"
        ],
        "attributes": {
            "size_oz": 2.7,
            "type": "antiperspirant",
            "protection_hours": 48
        },
        "retailers": ["target", "walmart", "cvs"],
        "image_url": "https://example.com/degree-men.jpg",
        "matches_womens": ["w009"]
    }
}


# =============================================================================
# CLOTHING PRODUCTS - Vanity Sizing Examples
# =============================================================================

WOMENS_CLOTHING = {
    "hm boyfriend hoodie": {
        "id": "wc001",
        "title": "H&M Women's Boyfriend Fit Hoodie",
        "price": 45.00,
        "category": "clothing",
        "subcategory": "hoodies",
        "brand": "H&M",
        "materials": ["80% cotton", "20% polyester"],
        "available_sizes": ["XS", "S", "M", "L", "XL"],
        "size_chart": {
            "XS": {"chest": 34, "waist": 26, "length": 24},
            "S": {"chest": 36, "waist": 28, "length": 25},
            "M": {"chest": 38, "waist": 30, "length": 26},
            "L": {"chest": 40, "waist": 32, "length": 27},
            "XL": {"chest": 42, "waist": 34, "length": 28}
        },
        "retailers": ["hm", "hm.com"],
        "image_url": "https://example.com/hm-womens-hoodie.jpg"
    },
    "uniqlo women sweatshirt": {
        "id": "wc002",
        "title": "Uniqlo Women's Sweat Pullover Long-Sleeve Shirt",
        "price": 39.90,
        "category": "clothing",
        "subcategory": "sweatshirts",
        "brand": "Uniqlo",
        "materials": ["100% cotton"],
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "size_chart": {
            "XS": {"chest": 33, "waist": 25, "length": 22},
            "S": {"chest": 35, "waist": 27, "length": 23},
            "M": {"chest": 37, "waist": 29, "length": 24},
            "L": {"chest": 39, "waist": 31, "length": 25},
            "XL": {"chest": 41, "waist": 33, "length": 26},
            "XXL": {"chest": 43, "waist": 35, "length": 27}
        },
        "retailers": ["uniqlo", "uniqlo.com"],
        "image_url": "https://example.com/uniqlo-womens.jpg"
    },
    "zara women tshirt": {
        "id": "wc003",
        "title": "Zara Women's Basic T-Shirt",
        "price": 25.90,
        "category": "clothing",
        "subcategory": "tshirts",
        "brand": "Zara",
        "materials": ["95% cotton", "5% elastane"],
        "available_sizes": ["XS", "S", "M", "L", "XL"],
        "size_chart": {
            "XS": {"chest": 32, "waist": 24, "length": 23},
            "S": {"chest": 34, "waist": 26, "length": 24},
            "M": {"chest": 36, "waist": 28, "length": 25},
            "L": {"chest": 38, "waist": 30, "length": 26},
            "XL": {"chest": 40, "waist": 32, "length": 27}
        },
        "retailers": ["zara", "zara.com"],
        "image_url": "https://example.com/zara-womens-tee.jpg"
    },
    "ae women jeans": {
        "id": "wc004",
        "title": "American Eagle Women's Mom Jeans",
        "price": 59.95,
        "category": "clothing",
        "subcategory": "jeans",
        "brand": "American Eagle",
        "materials": ["99% cotton", "1% elastane"],
        "available_sizes": ["00", "0", "2", "4", "6", "8", "10", "12", "14", "16"],
        "size_chart": {
            "00": {"waist": 23, "hip": 33, "inseam": 29},
            "0": {"waist": 24, "hip": 34, "inseam": 29},
            "2": {"waist": 25, "hip": 35, "inseam": 29},
            "4": {"waist": 26, "hip": 36, "inseam": 29},
            "6": {"waist": 27, "hip": 37, "inseam": 29},
            "8": {"waist": 28, "hip": 38, "inseam": 29},
            "10": {"waist": 29, "hip": 39, "inseam": 29},
            "12": {"waist": 30, "hip": 40, "inseam": 29},
            "14": {"waist": 32, "hip": 42, "inseam": 29},
            "16": {"waist": 34, "hip": 44, "inseam": 29}
        },
        "retailers": ["ae", "ae.com", "american eagle"],
        "image_url": "https://example.com/ae-womens-jeans.jpg"
    }
}

MENS_CLOTHING = {
    "hm basic hoodie": {
        "id": "mc001",
        "title": "H&M Men's Regular Fit Hoodie",
        "price": 24.99,
        "category": "clothing",
        "subcategory": "hoodies",
        "brand": "H&M",
        "materials": ["80% cotton", "20% polyester"],
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "size_chart": {
            "XS": {"chest": 34, "waist": 28, "length": 26},
            "S": {"chest": 36, "waist": 30, "length": 27},
            "M": {"chest": 38, "waist": 32, "length": 28},
            "L": {"chest": 40, "waist": 34, "length": 29},
            "XL": {"chest": 42, "waist": 36, "length": 30},
            "XXL": {"chest": 44, "waist": 38, "length": 31}
        },
        "retailers": ["hm", "hm.com"],
        "image_url": "https://example.com/hm-mens-hoodie.jpg",
        "matches_womens": ["wc001"]
    },
    "uniqlo men sweatshirt": {
        "id": "mc002",
        "title": "Uniqlo Men's Sweat Pullover Long-Sleeve Shirt",
        "price": 29.90,
        "category": "clothing",
        "subcategory": "sweatshirts",
        "brand": "Uniqlo",
        "materials": ["100% cotton"],
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL", "3XL"],
        "size_chart": {
            "XS": {"chest": 36, "waist": 30, "length": 25},
            "S": {"chest": 38, "waist": 32, "length": 26},
            "M": {"chest": 40, "waist": 34, "length": 27},
            "L": {"chest": 42, "waist": 36, "length": 28},
            "XL": {"chest": 44, "waist": 38, "length": 29},
            "XXL": {"chest": 46, "waist": 40, "length": 30},
            "3XL": {"chest": 48, "waist": 42, "length": 31}
        },
        "retailers": ["uniqlo", "uniqlo.com"],
        "image_url": "https://example.com/uniqlo-mens.jpg",
        "matches_womens": ["wc002"]
    },
    "zara men tshirt": {
        "id": "mc003",
        "title": "Zara Men's Basic T-Shirt",
        "price": 17.90,
        "category": "clothing",
        "subcategory": "tshirts",
        "brand": "Zara",
        "materials": ["100% cotton"],
        "available_sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "size_chart": {
            "XS": {"chest": 35, "waist": 29, "length": 26},
            "S": {"chest": 37, "waist": 31, "length": 27},
            "M": {"chest": 39, "waist": 33, "length": 28},
            "L": {"chest": 41, "waist": 35, "length": 29},
            "XL": {"chest": 43, "waist": 37, "length": 30},
            "XXL": {"chest": 45, "waist": 39, "length": 31}
        },
        "retailers": ["zara", "zara.com"],
        "image_url": "https://example.com/zara-mens-tee.jpg",
        "matches_womens": ["wc003"]
    },
    "ae men jeans": {
        "id": "mc004",
        "title": "American Eagle Men's Original Straight Jeans",
        "price": 49.95,
        "category": "clothing",
        "subcategory": "jeans",
        "brand": "American Eagle",
        "materials": ["99% cotton", "1% elastane"],
        "available_sizes": ["28x28", "28x30", "29x30", "30x30", "30x32", "31x30", "31x32",
                          "32x30", "32x32", "33x30", "33x32", "34x30", "34x32", "36x30", "36x32"],
        "size_chart": {
            "28x30": {"waist": 28, "hip": 36, "inseam": 30},
            "29x30": {"waist": 29, "hip": 37, "inseam": 30},
            "30x30": {"waist": 30, "hip": 38, "inseam": 30},
            "30x32": {"waist": 30, "hip": 38, "inseam": 32},
            "31x30": {"waist": 31, "hip": 39, "inseam": 30},
            "31x32": {"waist": 31, "hip": 39, "inseam": 32},
            "32x30": {"waist": 32, "hip": 40, "inseam": 30},
            "32x32": {"waist": 32, "hip": 40, "inseam": 32},
            "33x30": {"waist": 33, "hip": 41, "inseam": 30},
            "33x32": {"waist": 33, "hip": 41, "inseam": 32},
            "34x30": {"waist": 34, "hip": 42, "inseam": 30},
            "34x32": {"waist": 34, "hip": 42, "inseam": 32},
            "36x30": {"waist": 36, "hip": 44, "inseam": 30},
            "36x32": {"waist": 36, "hip": 44, "inseam": 32}
        },
        "retailers": ["ae", "ae.com", "american eagle"],
        "image_url": "https://example.com/ae-mens-jeans.jpg",
        "matches_womens": ["wc004"]
    }
}


# =============================================================================
# PRE-COMPUTED PRODUCT PAIRS (For instant demo responses)
# =============================================================================

GOLDEN_PAIRS = [
    {
        "womens_id": "w001",
        "mens_id": "m002",
        "similarity_score": 0.87,
        "match_reasons": [
            "Same blade count (5 blades)",
            "Both have aloe moisture strips",
            "Both have pivoting heads",
            "Same brand quality (Gillette)"
        ]
    },
    {
        "womens_id": "w003",
        "mens_id": "m003",
        "similarity_score": 0.91,
        "match_reasons": [
            "Identical first 3 active ingredients",
            "Both contain aloe vera",
            "Men's version is LARGER (10oz vs 7oz)",
            "Both designed for sensitive skin"
        ]
    },
    {
        "womens_id": "w005",
        "mens_id": "m005",
        "similarity_score": 0.94,
        "match_reasons": [
            "Identical active ingredient formula",
            "Same 48-hour protection",
            "Same antiperspirant type",
            "Same parent company (P&G)"
        ]
    },
    {
        "womens_id": "w006",
        "mens_id": "m006",
        "similarity_score": 0.98,
        "match_reasons": [
            "Identical soap formula",
            "Same bar count and size",
            "Same moisturizing technology",
            "Same brand - only color differs"
        ]
    },
    {
        "womens_id": "wc001",
        "mens_id": "mc001",
        "similarity_score": 0.95,
        "match_reasons": [
            "Identical material composition",
            "Same brand and quality",
            "Similar fit characteristics",
            "Only sizing system differs"
        ]
    },
    # New pairs for expanded demo
    {
        "womens_id": "w007",
        "mens_id": "m007",
        "similarity_score": 0.89,
        "match_reasons": [
            "Same brand and formula",
            "Identical first 5 ingredients",
            "Same size (3.3oz)",
            "Only fragrance differs"
        ]
    },
    {
        "womens_id": "w008",
        "mens_id": "m008",
        "similarity_score": 0.85,
        "match_reasons": [
            "Same blade count (5 blades)",
            "Both premium DTC brands",
            "Both have lubricating strips",
            "Harry's is 31% cheaper"
        ]
    },
    {
        "womens_id": "w009",
        "mens_id": "m009",
        "similarity_score": 0.96,
        "match_reasons": [
            "Same brand (Degree)",
            "Identical active ingredient",
            "Same 48-hour protection",
            "Men's has MORE product (2.7oz vs 2.6oz)"
        ]
    },
    {
        "womens_id": "wc002",
        "mens_id": "mc002",
        "similarity_score": 0.92,
        "match_reasons": [
            "Same brand (Uniqlo)",
            "Identical 100% cotton material",
            "Same quality construction",
            "Men's is 25% cheaper"
        ]
    },
    {
        "womens_id": "wc003",
        "mens_id": "mc003",
        "similarity_score": 0.90,
        "match_reasons": [
            "Same brand (Zara)",
            "Similar material composition",
            "Same product line",
            "Men's is 31% cheaper"
        ]
    },
    {
        "womens_id": "wc004",
        "mens_id": "mc004",
        "similarity_score": 0.88,
        "match_reasons": [
            "Same brand (American Eagle)",
            "Identical material (99% cotton, 1% elastane)",
            "Same quality denim",
            "Men's uses actual inch measurements"
        ]
    }
]


def get_all_womens_products():
    """Get all women's products (personal care + clothing)."""
    return {**WOMENS_PRODUCTS, **WOMENS_CLOTHING}


def get_all_mens_products():
    """Get all men's products (personal care + clothing)."""
    return {**MENS_PRODUCTS, **MENS_CLOTHING}


def get_golden_pair(womens_id: str) -> dict | None:
    """Get pre-computed pair data for a women's product."""
    for pair in GOLDEN_PAIRS:
        if pair["womens_id"] == womens_id:
            return pair
    return None


def find_matching_key(title: str, products_dict: dict) -> str | None:
    """
    Find the best matching product key based on title.

    Args:
        title: Product title to search for
        products_dict: Dictionary of products to search in

    Returns:
        The matching key if found, None otherwise
    """
    title_lower = title.lower()

    # First try exact key match
    for key in products_dict:
        if key in title_lower or title_lower in key:
            return key

    # Then try matching against product titles
    for key, product in products_dict.items():
        product_title = product.get("title", "").lower()
        if title_lower in product_title or product_title in title_lower:
            return key

    # Try word overlap for partial matches
    title_words = set(title_lower.split())
    best_match = None
    best_score = 0

    for key, product in products_dict.items():
        key_words = set(key.split())
        product_words = set(product.get("title", "").lower().split())
        all_words = key_words | product_words

        overlap = len(title_words & all_words)
        if overlap > best_score and overlap >= 2:
            best_score = overlap
            best_match = key

    return best_match
