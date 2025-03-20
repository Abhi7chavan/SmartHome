#master table infotmationtype sql query

"""
CREATE TABLE meta.informationtype (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(255) NOT NULL
);


INSERT INTO meta.informationtype (type) VALUES 
    ('electric'),
    ('water'),
    ('weather');
"""


"""
    INSERT INTO appliances (item_name, min_watt_range, max_watt_range)
VALUES
    ('Toaster', 800, 1200),
    ('Blender', 300, 700),
    ('Coffee Maker', 600, 1200),
    ('Microwave', 700, 1500),
    ('Electric Kettle', 1000, 1500),
    ('Refrigerator', 100, 200),
    ('Washing Machine', 500, 1000),
    ('Dryer', 1000, 4000),
    ('Dishwasher', 1200, 2400),
    ('Iron', 1000, 2000),
    ('Vacuum Cleaner', 500, 1500),
    ('Air Conditioner', 1000, 3000),
    ('Television', 50, 200),
    ('Laptop', 30, 90),
    ('Hair Dryer', 800, 1800),
    ('Toaster Oven', 1200, 1800),
    ('Fan', 50, 100),
    ('Heater', 1000, 3000),
    ('Clock Radio', 10, 30),
    ('Sewing Machine', 70, 150),
    ('Electric Razor', 10, 50),
    ('Food Processor', 300, 900),
    ('Alarm Clock', 5, 15),
    ('Electric Blanket', 200, 400),
    ('Smoke Detector', 5, 20),
    ('Hair Clippers', 15, 30),
    ('Curling Iron', 25, 50),
    ('Garbage Disposal', 300, 600),
    ('Space Heater', 1500, 2500),
    ('Electric Can Opener', 60, 100),
    ('Hand Mixer', 200, 400),
    ('Digital Clock', 10, 20);
    
    """