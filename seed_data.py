"""
Seed script to populate UYD database with sample programs and events
"""

from datetime import datetime, timedelta
from main import SessionLocal, Program, Event, NewsArticle

def seed_programs(db):
    """Seed the database with sample programs"""
    programs_data = [
        {
            "title": "Youth Education & Skills Development",
            "description": "Comprehensive education programs designed to equip young people with essential skills for the modern workforce.",
            "category": "education",
            "content": """
            Our Education & Skills Development program focuses on providing quality education and practical skills training to youth across Tanzania. The program includes:

            • Formal and informal education support
            • Vocational training in various trades
            • Digital literacy and computer skills
            • Entrepreneurship education
            • Life skills and personal development workshops
            • Career guidance and mentorship programs

            Through partnerships with local schools, vocational centers, and industry leaders, we ensure our participants receive relevant, market-driven education that prepares them for successful careers.
            """,
            "featured_image": "/assets/img/education/education-1.webp",
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Agribusiness & Sustainable Farming",
            "description": "Empowering youth through sustainable agriculture practices and agribusiness entrepreneurship.",
            "category": "agribusiness",
            "content": """
            Our Agribusiness program transforms young people's perception of agriculture from subsistence farming to profitable entrepreneurship. Key components include:

            • Modern farming techniques and technologies
            • Value chain development and market linkages
            • Climate-smart agriculture practices
            • Agribusiness management and entrepreneurship
            • Cooperative formation and management
            • Access to finance and business development services

            Participants learn to create sustainable agricultural businesses that contribute to food security and economic development in their communities.
            """,
            "featured_image": "/assets/img/education/agribusiness-1.webp",
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Youth Leadership Development",
            "description": "Building confident leaders who drive positive change in their communities and beyond.",
            "category": "leadership",
            "content": """
            Our Leadership Development program cultivates the next generation of change-makers through comprehensive leadership training:

            • Leadership theory and practice
            • Community mobilization and advocacy
            • Project planning and management
            • Conflict resolution and mediation
            • Public speaking and communication skills
            • Youth policy and governance

            Graduates of our leadership programs become catalysts for positive change, implementing community projects and advocating for youth issues at local and national levels.
            """,
            "featured_image": "/assets/img/education/leadership-1.webp",
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Environmental Conservation & Climate Action",
            "description": "Youth-led initiatives for environmental protection and climate change adaptation.",
            "category": "environment",
            "content": """
            Our Environmental Conservation program engages youth in protecting Tanzania's rich biodiversity and addressing climate change:

            • Reforestation and watershed management
            • Climate change education and awareness
            • Sustainable resource management
            • Environmental entrepreneurship
            • Disaster risk reduction
            • Eco-tourism development

            Through hands-on projects and education, participants become environmental stewards who protect their communities and contribute to global climate action.
            """,
            "featured_image": "/assets/img/education/environment-1.webp",
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Tourism & Cultural Heritage",
            "description": "Promoting cultural tourism and heritage conservation among Tanzanian youth.",
            "category": "tourism",
            "content": """
            Our Tourism program celebrates Tanzania's rich cultural heritage while creating economic opportunities:

            • Cultural tourism product development
            • Heritage conservation and management
            • Tourism entrepreneurship
            • Customer service and hospitality skills
            • Cultural performance and arts
            • Community-based tourism initiatives

            Participants learn to showcase Tanzania's cultural diversity while creating sustainable tourism businesses that benefit their communities.
            """,
            "featured_image": "/assets/img/education/tourism-1.webp",
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Life Skills & Personal Development",
            "description": "Essential life skills training for holistic youth development and well-being.",
            "category": "lifeskills",
            "content": """
            Our Life Skills program addresses the holistic development needs of young people:

            • Financial literacy and money management
            • Health and wellness education
            • Gender equality and reproductive health
            • Mental health and stress management
            • Relationship building and communication
            • Time management and goal setting

            These essential skills empower youth to make informed decisions, maintain healthy relationships, and achieve their personal and professional goals.
            """,
            "featured_image": "/assets/img/education/lifeskills-1.webp",
            "is_featured": False,
            "is_active": True
        }
    ]

    for program_data in programs_data:
        program = Program(**program_data)
        db.add(program)

    db.commit()
    print(f"Seeded {len(programs_data)} programs")

def seed_events(db):
    """Seed the database with sample events"""
    base_date = datetime.utcnow()

    events_data = [
        {
            "title": "Annual Science Exhibition",
            "description": "Showcase of innovative projects and scientific discoveries by UYD participants",
            "event_type": "exhibition",
            "start_date": base_date + timedelta(days=15),
            "end_date": base_date + timedelta(days=16),
            "location": "Main Campus Auditorium",
            "max_participants": 200,
            "featured_image": "/assets/img/education/events-1.webp",
            "content": "Join us for our annual showcase of scientific innovation and discovery. Participants will present projects in science, technology, engineering, and mathematics.",
            "registration_deadline": base_date + timedelta(days=10),
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Parent-Teacher Conference",
            "description": "Building stronger partnerships between parents, teachers, and youth for better educational outcomes",
            "event_type": "conference",
            "start_date": base_date + timedelta(days=22),
            "location": "School Conference Center",
            "max_participants": 150,
            "featured_image": "/assets/img/education/events-2.webp",
            "content": "An important gathering to discuss student progress, challenges, and strategies for supporting youth development.",
            "registration_deadline": base_date + timedelta(days=18),
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Annual Sports Tournament",
            "description": "Inter-school and community sports competition promoting physical fitness and teamwork",
            "event_type": "sports",
            "start_date": base_date + timedelta(days=35),
            "end_date": base_date + timedelta(days=37),
            "location": "Campus Sports Ground",
            "max_participants": 300,
            "featured_image": "/assets/img/education/events-3.webp",
            "content": "A celebration of athletic excellence featuring football, basketball, volleyball, and track & field events.",
            "registration_deadline": base_date + timedelta(days=25),
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Graduation Ceremony 2025",
            "description": "Celebrating the achievements of our program graduates",
            "event_type": "ceremony",
            "start_date": base_date + timedelta(days=50),
            "location": "University Grand Hall",
            "max_participants": 500,
            "featured_image": "/assets/img/education/events-4.webp",
            "content": "A momentous occasion honoring the hard work and dedication of our graduates as they embark on their next chapter.",
            "registration_deadline": base_date + timedelta(days=45),
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Summer Leadership Camp",
            "description": "Intensive leadership training and team-building experience for youth leaders",
            "event_type": "camp",
            "start_date": base_date + timedelta(days=70),
            "end_date": base_date + timedelta(days=75),
            "location": "Mountain Resort, Moshi",
            "max_participants": 50,
            "featured_image": "/assets/img/education/events-5.webp",
            "content": "A transformative week of leadership development, outdoor activities, and community service projects.",
            "registration_deadline": base_date + timedelta(days=60),
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Agribusiness Workshop Series",
            "description": "Hands-on training in modern farming techniques and business development",
            "event_type": "workshop",
            "start_date": base_date + timedelta(days=10),
            "end_date": base_date + timedelta(days=12),
            "location": "Agricultural Training Center",
            "max_participants": 30,
            "featured_image": "/assets/img/education/events-6.webp",
            "content": "Learn practical skills in crop production, livestock management, and agricultural entrepreneurship.",
            "registration_deadline": base_date + timedelta(days=5),
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Environmental Conservation Summit",
            "description": "Youth voices on climate action and environmental protection",
            "event_type": "summit",
            "start_date": base_date + timedelta(days=40),
            "location": "National Environment Center",
            "max_participants": 100,
            "featured_image": "/assets/img/education/events-7.webp",
            "content": "A platform for young environmental activists to share solutions and advocate for policy changes.",
            "registration_deadline": base_date + timedelta(days=35),
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Youth Entrepreneurship Fair",
            "description": "Showcase of youth-led businesses and innovative startup ideas",
            "event_type": "fair",
            "start_date": base_date + timedelta(days=55),
            "location": "Business Innovation Hub",
            "max_participants": 200,
            "featured_image": "/assets/img/education/events-8.webp",
            "content": "Connect with investors, mentors, and fellow entrepreneurs while showcasing your business ideas.",
            "registration_deadline": base_date + timedelta(days=50),
            "is_featured": False,
            "is_active": True
        }
    ]

    for event_data in events_data:
        event = Event(**event_data)
        db.add(event)

    db.commit()
    print(f"Seeded {len(events_data)} events")

def seed_news(db):
    """Seed the database with sample news articles"""
    base_date = datetime.utcnow()

    news_data = [
        {
            "title": "UYD Graduates Make Impact in Local Communities",
            "content": "Twenty-five graduates from our leadership program have successfully implemented community projects across three districts, demonstrating the real-world impact of our training initiatives.",
            "excerpt": "Leadership program graduates implement successful community projects in multiple districts.",
            "category": "success",
            "author": "UYD Communications Team",
            "publish_date": base_date - timedelta(days=5),
            "featured_image": "/assets/img/blog/blog-post-1.webp",
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "New Partnership with Agricultural Ministry",
            "content": "United Youth Developers signs memorandum of understanding with Ministry of Agriculture to expand agribusiness training programs nationwide.",
            "excerpt": "Strategic partnership to scale up youth agribusiness training across Tanzania.",
            "category": "partnership",
            "author": "UYD Communications Team",
            "publish_date": base_date - timedelta(days=12),
            "featured_image": "/assets/img/blog/blog-post-2.webp",
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Environmental Club Plants 10,000 Trees",
            "content": "UYD environmental conservation program achieves milestone with successful reforestation project in Mount Kilimanjaro region.",
            "excerpt": "Major reforestation achievement in Kilimanjaro region contributes to climate action goals.",
            "category": "environment",
            "author": "UYD Communications Team",
            "publish_date": base_date - timedelta(days=20),
            "featured_image": "/assets/img/blog/blog-post-3.webp",
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Youth Leadership Summit 2025 Announced",
            "content": "Preparations underway for the annual Youth Leadership Summit featuring international speakers and workshops on entrepreneurship and innovation.",
            "excerpt": "Annual leadership summit to bring together youth leaders from across East Africa.",
            "category": "events",
            "author": "UYD Communications Team",
            "publish_date": base_date - timedelta(days=25),
            "featured_image": "/assets/img/blog/blog-post-4.webp",
            "is_featured": True,
            "is_active": True
        }
    ]

    for news_item in news_data:
        article = NewsArticle(**news_item)
        db.add(article)

    db.commit()
    print(f"Seeded {len(news_data)} news articles")

def main():
    """Main seeding function"""
    db = SessionLocal()
    try:
        print("Starting database seeding...")

        # Clear existing data (optional - comment out if you want to keep existing data)
        db.query(Program).delete()
        db.query(Event).delete()
        db.query(NewsArticle).delete()
        db.commit()

        # Seed data
        seed_programs(db)
        seed_events(db)
        seed_news(db)

        print("Database seeding completed successfully!")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()


