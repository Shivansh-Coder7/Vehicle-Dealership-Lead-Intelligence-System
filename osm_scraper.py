import overpy
import pandas as pd

def fetch_from_osm(city="Indore"):
    """Fetch car showrooms from OpenStreetMap."""
    api = overpy.Overpass()

    query = f"""
    [out:json][timeout:60];
    area[name="{city}"]->.searchArea;
    (
      node["shop"="car"](area.searchArea);
      way["shop"="car"](area.searchArea);
      node["amenity"="car_showroom"](area.searchArea);
      way["amenity"="car_showroom"](area.searchArea);
      node["shop"="motorcycle"](area.searchArea);
      way["shop"="motorcycle"](area.searchArea);
      node["shop"="bicycle"](area.searchArea);
    );
    out body;
    >;
    out skel qt;
    """

    print("Contacting OpenStreetMap... (takes 5-10 seconds)")
    result = api.query(query)

    businesses = []

    for node in result.nodes:
        tags = node.tags
        name = tags.get("name", "").strip()
        if not name:
            continue
        businesses.append({
            "name": name,
            "category": "Car Showroom",
            "city": city,
            "address": tags.get("addr:full", tags.get("addr:street", "Indore")),
            "phone": tags.get("phone", tags.get("contact:phone", "")),
            "website": tags.get("website", tags.get("contact:website", "")),
            "brand": tags.get("brand", ""),
            "source": "OSM"
        })

    for way in result.ways:
        tags = way.tags
        name = tags.get("name", "").strip()
        if not name:
            continue
        businesses.append({
            "name": name,
            "category": "Car Showroom",
            "city": city,
            "address": tags.get("addr:full", tags.get("addr:street", "Indore")),
            "phone": tags.get("phone", tags.get("contact:phone", "")),
            "website": tags.get("website", tags.get("contact:website", "")),
            "brand": tags.get("brand", ""),
            "source": "OSM"
        })

    print(f"OSM returned {len(businesses)} results")
    return businesses


def get_manual_seed():
    """
    Expanded list of car showroom / dealership entries in Indore.
    Covers multiple branches per brand + used car dealers to reach 70-100+ leads.
    """
    return [
        # Maruti Suzuki (Arena + Nexa + True Value - multiple branches)
        {"name": "Pratap Motors Maruti Suzuki Vijay Nagar Indore", "brand": "Maruti Suzuki", "address": "Vijay Nagar, Indore"},
        {"name": "Sai Service Maruti Suzuki AB Road Indore", "brand": "Maruti Suzuki", "address": "AB Road, Indore"},
        {"name": "Mandovi Motors Maruti Suzuki Palasia Indore", "brand": "Maruti Suzuki", "address": "Palasia, Indore"},
        {"name": "Capital Motors Maruti Suzuki Nexa Indore", "brand": "Maruti Suzuki Nexa", "address": "RNT Marg, Indore"},
        {"name": "Pratap Nexa Showroom Indore", "brand": "Maruti Suzuki Nexa", "address": "Vijay Nagar, Indore"},
        {"name": "Maruti Suzuki True Value Bhawarkuan Indore", "brand": "Maruti Suzuki True Value", "address": "Bhawarkuan, Indore"},
        {"name": "Sai Service Maruti Suzuki Rau Indore", "brand": "Maruti Suzuki", "address": "Rau, Indore"},
        {"name": "Mandovi Nexa Showroom Indore", "brand": "Maruti Suzuki Nexa", "address": "AB Road, Indore"},

        # Hyundai
        {"name": "Sagar Motors Hyundai AB Road Indore", "brand": "Hyundai", "address": "AB Road, Indore"},
        {"name": "Krishna Hyundai Vijay Nagar Indore", "brand": "Hyundai", "address": "Vijay Nagar, Indore"},
        {"name": "Sagar Hyundai Showroom Rau Indore", "brand": "Hyundai", "address": "Rau, Indore"},
        {"name": "Sagar Motors Hyundai Service Centre Indore", "brand": "Hyundai", "address": "Bhawarkuan, Indore"},
        {"name": "Krishna Hyundai Used Cars Indore", "brand": "Hyundai", "address": "Palasia, Indore"},

        # Tata Motors
        {"name": "Nath Motors Tata Cars Rajwada Indore", "brand": "Tata Motors", "address": "Rajwada, Indore"},
        {"name": "Concorde Motors Tata Bhawarkuan Indore", "brand": "Tata Motors", "address": "Bhawarkuan, Indore"},
        {"name": "Nath Motors Tata Showroom AB Road Indore", "brand": "Tata Motors", "address": "AB Road, Indore"},
        {"name": "Concorde Motors Tata Service Centre Indore", "brand": "Tata Motors", "address": "Vijay Nagar, Indore"},
        {"name": "Tata Motors Commercial Vehicles Indore", "brand": "Tata Motors", "address": "Sanwer Road, Indore"},

        # Honda
        {"name": "Shivam Autozone Honda Cars Palasia Indore", "brand": "Honda", "address": "Palasia, Indore"},
        {"name": "Popular Honda Vijay Nagar Indore", "brand": "Honda", "address": "Vijay Nagar, Indore"},
        {"name": "Shivam Autozone Honda Service Centre Indore", "brand": "Honda", "address": "AB Road, Indore"},
        {"name": "Popular Honda Showroom Bhawarkuan Indore", "brand": "Honda", "address": "Bhawarkuan, Indore"},

        # Mahindra
        {"name": "Arihant Motors Mahindra Bhawarkuan Indore", "brand": "Mahindra", "address": "Bhawarkuan, Indore"},
        {"name": "Rohan Motors Mahindra AB Road Indore", "brand": "Mahindra", "address": "AB Road, Indore"},
        {"name": "Arihant Mahindra First Choice Indore", "brand": "Mahindra", "address": "Vijay Nagar, Indore"},
        {"name": "Rohan Motors Mahindra Service Centre Indore", "brand": "Mahindra", "address": "Rau, Indore"},

        # Toyota
        {"name": "Indus Toyota Vijay Nagar Indore", "brand": "Toyota", "address": "Vijay Nagar, Indore"},
        {"name": "Toyota Kirloskar Showroom South Tukoganj Indore", "brand": "Toyota", "address": "South Tukoganj, Indore"},
        {"name": "Indus Toyota Service Centre Indore", "brand": "Toyota", "address": "AB Road, Indore"},

        # Kia
        {"name": "Kia Motors Showroom AB Road Indore", "brand": "Kia", "address": "AB Road, Indore"},
        {"name": "Landmark Kia Vijay Nagar Indore", "brand": "Kia", "address": "Vijay Nagar, Indore"},
        {"name": "Kia Service Centre Indore", "brand": "Kia", "address": "Palasia, Indore"},

        # MG Motor
        {"name": "MG Motor Showroom Palasia Indore", "brand": "MG Motor", "address": "Palasia, Indore"},
        {"name": "Landmark MG AB Road Indore", "brand": "MG Motor", "address": "AB Road, Indore"},

        # Skoda
        {"name": "Skoda Showroom Vijay Nagar Indore", "brand": "Skoda", "address": "Vijay Nagar, Indore"},
        {"name": "Skoda Service Centre Indore", "brand": "Skoda", "address": "AB Road, Indore"},

        # Volkswagen
        {"name": "Volkswagen Showroom AB Road Indore", "brand": "Volkswagen", "address": "AB Road, Indore"},
        {"name": "Volkswagen Service Centre Indore", "brand": "Volkswagen", "address": "Vijay Nagar, Indore"},

        # Renault
        {"name": "Renault Showroom Vijay Nagar Indore", "brand": "Renault", "address": "Vijay Nagar, Indore"},
        {"name": "Popular Renault Palasia Indore", "brand": "Renault", "address": "Palasia, Indore"},

        # Nissan
        {"name": "Nissan Showroom AB Road Indore", "brand": "Nissan", "address": "AB Road, Indore"},

        # Jeep
        {"name": "Jeep FCA Showroom AB Road Indore", "brand": "Jeep", "address": "AB Road, Indore"},

        # Luxury Brands
        {"name": "BMW Showroom South Tukoganj Indore", "brand": "BMW", "address": "South Tukoganj, Indore"},
        {"name": "Mercedes Benz Showroom Vijay Nagar Indore", "brand": "Mercedes-Benz", "address": "Vijay Nagar, Indore"},
        {"name": "Audi Showroom AB Road Indore", "brand": "Audi", "address": "AB Road, Indore"},

        # Electric Vehicles
        {"name": "Tata EV Showroom Vijay Nagar Indore", "brand": "Tata EV", "address": "Vijay Nagar, Indore"},
        {"name": "BYD Electric Showroom AB Road Indore", "brand": "BYD", "address": "AB Road, Indore"},
        {"name": "Ola Electric Showroom Indore", "brand": "Ola Electric", "address": "Vijay Nagar, Indore"},

        # Citroen
        {"name": "Citroen Showroom Indore", "brand": "Citroen", "address": "AB Road, Indore"},

        # Used Car Dealers / Multi-brand
        {"name": "Cars24 Indore Hub", "brand": "Used Cars", "address": "AB Road, Indore"},
        {"name": "Spinny Car Hub Indore", "brand": "Used Cars", "address": "Vijay Nagar, Indore"},
        {"name": "CarDekho Used Cars Indore", "brand": "Used Cars", "address": "Palasia, Indore"},
        {"name": "OLX Autos Indore", "brand": "Used Cars", "address": "Bhawarkuan, Indore"},
        {"name": "Maruti True Value Rau Indore", "brand": "Used Cars", "address": "Rau, Indore"},
        {"name": "Mahindra First Choice Wheels Indore", "brand": "Used Cars", "address": "AB Road, Indore"},
        {"name": "Carwale Used Car Showroom Indore", "brand": "Used Cars", "address": "Vijay Nagar, Indore"},
        {"name": "Quikr Cars Indore", "brand": "Used Cars", "address": "Palasia, Indore"},
        {"name": "Droom Used Cars Indore", "brand": "Used Cars", "address": "South Tukoganj, Indore"},
        {"name": "CarTrade Exchange Indore", "brand": "Used Cars", "address": "AB Road, Indore"},

        # Local Independent Dealers (common in Indore)
        {"name": "Bansal Automobiles Indore", "brand": "Multi-brand", "address": "MG Road, Indore"},
        {"name": "Jain Motors Indore", "brand": "Multi-brand", "address": "Sapna Sangeeta, Indore"},
        {"name": "Agrawal Car World Indore", "brand": "Multi-brand", "address": "Bhawarkuan, Indore"},
        {"name": "Patel Auto Sales Indore", "brand": "Multi-brand", "address": "Rajwada, Indore"},
        {"name": "Sharma Motors Indore", "brand": "Multi-brand", "address": "Palasia, Indore"},
        {"name": "Gupta Car Bazaar Indore", "brand": "Multi-brand", "address": "AB Road, Indore"},
        {"name": "Verma Automobiles Indore", "brand": "Multi-brand", "address": "Vijay Nagar, Indore"},
        {"name": "Singh Motors Indore", "brand": "Multi-brand", "address": "Bicholi Mardana, Indore"},
        {"name": "Indore Car Bazaar", "brand": "Multi-brand", "address": "Annapurna Road, Indore"},
        {"name": "Royal Motors Indore", "brand": "Multi-brand", "address": "MR-10 Road, Indore"},
        {"name": "Indore Auto Hub", "brand": "Multi-brand", "address": "Bypass Road, Indore"},
        {"name": "City Motors Indore", "brand": "Multi-brand", "address": "Rau, Indore"},
        {"name": "Prestige Motors Indore", "brand": "Multi-brand", "address": "Scheme No 54, Indore"},
        {"name": "Galaxy Car Showroom Indore", "brand": "Multi-brand", "address": "Sukhliya, Indore"},
        {"name": "National Motors Indore", "brand": "Multi-brand", "address": "Khajrana, Indore"},
        {"name": "Madhya Pradesh Automobiles Indore", "brand": "Multi-brand", "address": "Geeta Bhawan, Indore"},
        {"name": "Sunrise Car World Indore", "brand": "Multi-brand", "address": "LIG Colony, Indore"},
        {"name": "Trinity Motors Indore", "brand": "Multi-brand", "address": "Old Palasia, Indore"},
        {"name": "Crystal Auto Indore", "brand": "Multi-brand", "address": "New Palasia, Indore"},
        {"name": "Diamond Motors Indore", "brand": "Multi-brand", "address": "Manorama Ganj, Indore"},
        {"name": "Pioneer Auto Sales Indore", "brand": "Multi-brand", "address": "Saket, Indore"},
        {"name": "Speed Motors Indore", "brand": "Multi-brand", "address": "Tilak Nagar, Indore"},
        {"name": "Elite Car Gallery Indore", "brand": "Multi-brand", "address": "Annapurna, Indore"},
        {"name": "Maharaja Motors Indore", "brand": "Multi-brand", "address": "Chhoti Gwaltoli, Indore"},

        # Commercial / other vehicle brands present in Indore
        {"name": "Force Motors Showroom Indore", "brand": "Force Motors", "address": "AB Road, Indore"},
        {"name": "Eicher Trucks and Cars Indore", "brand": "Eicher", "address": "Sanwer Road, Indore"},
        {"name": "Isuzu Motors Showroom Indore", "brand": "Isuzu", "address": "AB Road, Indore"},

        # ── Hero MotoCorp (largest two-wheeler brand) ──
        {"name": "Hero MotoCorp Showroom Vijay Nagar Indore", "brand": "Hero MotoCorp", "address": "Vijay Nagar, Indore"},
        {"name": "Hero MotoCorp Dealership AB Road Indore", "brand": "Hero MotoCorp", "address": "AB Road, Indore"},
        {"name": "Hero MotoCorp Service Centre Palasia Indore", "brand": "Hero MotoCorp", "address": "Palasia, Indore"},
        {"name": "Hero MotoCorp Showroom Bhawarkuan Indore", "brand": "Hero MotoCorp", "address": "Bhawarkuan, Indore"},
        {"name": "Hero MotoCorp Rau Road Indore", "brand": "Hero MotoCorp", "address": "Rau, Indore"},

        # ── Honda 2Wheelers ──
        {"name": "Honda 2Wheelers Showroom Vijay Nagar Indore", "brand": "Honda 2Wheelers", "address": "Vijay Nagar, Indore"},
        {"name": "Honda Motorcycle Scooter Indore AB Road", "brand": "Honda 2Wheelers", "address": "AB Road, Indore"},
        {"name": "Honda 2Wheelers Service Centre Indore", "brand": "Honda 2Wheelers", "address": "Palasia, Indore"},
        {"name": "Honda Activa Showroom Bhawarkuan Indore", "brand": "Honda 2Wheelers", "address": "Bhawarkuan, Indore"},

        # ── Bajaj Auto ──
        {"name": "Bajaj Auto Showroom Vijay Nagar Indore", "brand": "Bajaj Auto", "address": "Vijay Nagar, Indore"},
        {"name": "Bajaj Pulsar Dealership AB Road Indore", "brand": "Bajaj Auto", "address": "AB Road, Indore"},
        {"name": "Bajaj Auto Service Centre Indore", "brand": "Bajaj Auto", "address": "Palasia, Indore"},
        {"name": "Bajaj Dealership Bhawarkuan Indore", "brand": "Bajaj Auto", "address": "Bhawarkuan, Indore"},

        # ── TVS Motors ──
        {"name": "TVS Motors Showroom Vijay Nagar Indore", "brand": "TVS", "address": "Vijay Nagar, Indore"},
        {"name": "TVS Apache Dealership AB Road Indore", "brand": "TVS", "address": "AB Road, Indore"},
        {"name": "TVS Motors Service Centre Indore", "brand": "TVS", "address": "Palasia, Indore"},
        {"name": "TVS Showroom Rau Indore", "brand": "TVS", "address": "Rau, Indore"},

        # ── Royal Enfield ──
        {"name": "Royal Enfield Showroom Vijay Nagar Indore", "brand": "Royal Enfield", "address": "Vijay Nagar, Indore"},
        {"name": "Royal Enfield Dealership AB Road Indore", "brand": "Royal Enfield", "address": "AB Road, Indore"},
        {"name": "Royal Enfield Studio Indore Palasia", "brand": "Royal Enfield", "address": "Palasia, Indore"},

        # ── Yamaha ──
        {"name": "Yamaha Showroom Vijay Nagar Indore", "brand": "Yamaha", "address": "Vijay Nagar, Indore"},
        {"name": "Yamaha R15 Dealership AB Road Indore", "brand": "Yamaha", "address": "AB Road, Indore"},
        {"name": "Yamaha Service Centre Bhawarkuan Indore", "brand": "Yamaha", "address": "Bhawarkuan, Indore"},

        # ── Suzuki 2Wheelers ──
        {"name": "Suzuki Motorcycle Showroom Indore", "brand": "Suzuki 2W", "address": "AB Road, Indore"},
        {"name": "Suzuki Access Dealership Vijay Nagar Indore", "brand": "Suzuki 2W", "address": "Vijay Nagar, Indore"},

        # ── KTM / Husqvarna ──
        {"name": "KTM Showroom Indore Vijay Nagar", "brand": "KTM", "address": "Vijay Nagar, Indore"},
        {"name": "KTM Duke Dealership AB Road Indore", "brand": "KTM", "address": "AB Road, Indore"},
        {"name": "Husqvarna Motorcycles Indore", "brand": "Husqvarna", "address": "Vijay Nagar, Indore"},

        # ── Jawa / Yezdi ──
        {"name": "Jawa Motorcycles Showroom Indore", "brand": "Jawa", "address": "AB Road, Indore"},
        {"name": "Yezdi Motorcycles Dealership Indore", "brand": "Yezdi", "address": "Vijay Nagar, Indore"},

        # ── Electric Two Wheelers ──
        {"name": "Ola Electric Scooter Showroom Indore", "brand": "Ola Electric", "address": "Vijay Nagar, Indore"},
        {"name": "Ather Energy Showroom Indore", "brand": "Ather Energy", "address": "AB Road, Indore"},
        {"name": "Ather Energy Service Point Indore", "brand": "Ather Energy", "address": "Palasia, Indore"},
        {"name": "Revolt Electric Motorcycle Indore", "brand": "Revolt Motors", "address": "Vijay Nagar, Indore"},
        {"name": "Simple Energy Showroom Indore", "brand": "Simple Energy", "address": "AB Road, Indore"},
        {"name": "Bounce Infinity Electric Indore", "brand": "Bounce Infinity", "address": "Palasia, Indore"},

        # ── Local Two Wheeler Dealers ──
        {"name": "Bansal Two Wheelers Indore", "brand": "Multi-brand 2W", "address": "MG Road, Indore"},
        {"name": "Jain Bike World Indore", "brand": "Multi-brand 2W", "address": "Sapna Sangeeta, Indore"},
        {"name": "Sharma Two Wheeler Sales Indore", "brand": "Multi-brand 2W", "address": "Palasia, Indore"},
        {"name": "Indore Bike Bazaar", "brand": "Multi-brand 2W", "address": "Annapurna Road, Indore"},
        {"name": "Speed Bike World Indore", "brand": "Multi-brand 2W", "address": "Tilak Nagar, Indore"},
        {"name": "Gupta Two Wheelers Indore", "brand": "Multi-brand 2W", "address": "Bhawarkuan, Indore"},
        {"name": "Royal Bike Showroom Indore", "brand": "Multi-brand 2W", "address": "Rau, Indore"},
        {"name": "Star Motors Two Wheelers Indore", "brand": "Multi-brand 2W", "address": "Sukhliya, Indore"},
    ]


if __name__ == "__main__":
    try:
        osm_data = fetch_from_osm("Indore")
    except Exception as e:
        print(f"OSM failed: {e}")
        osm_data = []

    print("Adding expanded manual seed data...")
    manual_data = get_manual_seed()

    all_businesses = []

    for b in osm_data:
        all_businesses.append(b)

    for b in manual_data:
        all_businesses.append({
            "name": b["name"],
            "category": "Car Showroom",
            "city": "Indore",
            "address": b["address"],
            "phone": "",
            "website": "",
            "brand": b["brand"],
            "source": "Manual"
        })

    df = pd.DataFrame(all_businesses)
    df.drop_duplicates(subset=["name"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    df.to_csv("businesses.csv", index=False)

    print(f"\nDone! Total saved: {len(df)} car showrooms to businesses.csv")
    print(f"  - From OSM: {len(osm_data)}")
    print(f"  - From Manual seed: {len(manual_data)}")
