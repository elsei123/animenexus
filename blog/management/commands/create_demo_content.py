import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from blog.models import Post, Category

class Command(BaseCommand):
    """
    Command to create demo posts in the database based on provided content.
    It creates an author user (if it does not exist), categories,
    and various categorized posts, each with an associated image.
    """

    help = 'Creates demo posts based on provided content.'

    def handle(self, *args, **options):
        # Create an author user if it does not exist
        author, created = User.objects.get_or_create(username='admin')
        if created:
            author.set_password('admin')  # Use uma senha segura em produção
            author.is_superuser = True
            author.is_staff = True
            author.save()
            self.stdout.write(self.style.SUCCESS('Admin user criado.'))

        # Define categorias e suas descrições
        categories_data = {
            'Best of All Time': 'Top Classic Anime',
            'Worst of All Time': 'Worst Anime',
            'Best of the Year': 'Top Anime of the Year',
            'Worst of the Year': 'Worst Anime of the Year',
            'Upcoming Releases': 'Anime Set to Premiere',
            'Best Movies': 'Must-Watch Films',
            'Annual Winners': 'Award-Winning Anime',
        }

        # Criar categorias
        cats = {}
        for name, desc in categories_data.items():
            c, _ = Category.objects.get_or_create(name=name, description=desc)
            cats[name] = c
            self.stdout.write(self.style.SUCCESS(f'Categoria "{name}" criada.'))

        media_path = os.path.join(settings.MEDIA_ROOT, 'posts')

        if not os.path.exists(media_path):
            self.stdout.write(self.style.ERROR('Media directory not found.'))
            return

        def create_post(title, content, category, image_name):
            """
            Creates a Post object in the database, associating it with an image.
            If the specified image does not exist, it uses 'placeholder.jpg'.

            :param title: Post title
            :param content: Post content (text)
            :param category: Category object to which the post belongs
            :param image_name: Image file name
            """
            image_path = os.path.join(media_path, image_name)
            if not os.path.exists(image_path):
                # If the image is not found, use placeholder
                placeholder = 'placeholder.jpg'
                image_path = os.path.join(media_path, placeholder)
                if not os.path.exists(image_path):
                    # If no placeholder exists, raise an error
                    self.stdout.write(self.style.ERROR(
                        f'Imagem placeholder "{placeholder}" não encontrada.'))
                    return
                self.stdout.write(self.style.WARNING(
                    f'Imagem "{image_name}" não encontrada, usando "{placeholder}".'))
            with open(image_path, 'rb') as img_file:
                post = Post(
                    title=title,
                    content=content,
                    author=author,
                    category=category
                )
                post.cover_image.save(image_name, img_file, save=True)
            self.stdout.write(self.style.SUCCESS(f'Post "{title}" criado.'))
            return post

        # Best of All Time (Top 5) - longer descriptions
        best_ever = [
            (
                "Fullmetal Alchemist: Brotherhood",
                """Fullmetal Alchemist: Brotherhood is often considered the pinnacle of shounen anime.
The story follows the Elric brothers on a deep journey of redemption after a failed
attempt at human transmutation. Beyond its intense adventure, the anime explores morality,
sacrifice, and the search for the meaning of life. Each character is three-dimensional, and
the balance between drama, humor, and action is flawless. I recommend it for its captivating
storytelling, inspiring message, and notable technical quality that remains consistent
from start to finish.""",
                "fullmetal.jpg"
            ),
            (
                "Neon Genesis Evangelion",
                """Neon Genesis Evangelion revolutionized the mecha genre by diving into the psyche
of its characters. The series is not just about giant robots but explores themes of loneliness,
fear of abandonment, and the search for acceptance. Religious and philosophical symbolism
permeates every episode, creating multiple layers of interpretation. The emotional claustrophobia
and the tension between the pilots and the NERV organization define the experience.
I recommend this anime for its bold narrative, cultural influence, and the reflection it provokes
on the human condition.""",
                "evangelion.jpg"
            ),
            (
                "Monster",
                """Monster is a unique psychological thriller focused on the pursuit between Dr. Tenma
and the enigmatic Johan. Instead of magic or special powers, the story is grounded in realism
and moral complexity. Each secondary character is carefully constructed, adding depth to the
world and the dilemmas faced. The plot questions the value of life, the weight of responsibility,
and what makes us human. The slow and dense narrative rewards the viewer with an intense
and unforgettable experience.""",
                "monster.jpg"
            ),
            (
                "Gintama",
                """Gintama is the perfect mix of comedy, satire, and action. Set in a feudal Japan
dominated by aliens, the series plays with genre conventions, breaks the fourth wall,
and makes numerous pop culture references. But don’t be fooled: behind the nonsensical humor,
there are dramatic and emotional arcs that explore loyalty, friendship, and redemption.
The characters are charismatic and evolve throughout the story. Gintama surprises with its
versatility, capable of making you laugh uncontrollably and cry from pure emotion.""",
                "gintama.jpg"
            ),
            (
                "Death Note",
                """Death Note is an intellectual duel between two geniuses: Light Yagami, who discovers
a notebook capable of killing anyone whose name is written in it, and L, the eccentric detective
who tries to stop him. The anime makes us question what justice is and how far we can go to achieve it.
The constant tension, dark atmosphere, and meticulous strategies of the characters make every
episode gripping. The moral battle between absolute power and responsibility is its greatest strength.
I recommend it for its intensity and the ethical reflection it inspires about humanity.""",
                "deathnote.jpg"
            ),
        ]
        for title, desc, img in best_ever:
            create_post(title, desc, cats['Best of All Time'], img)

        # Worst of All Time (Top 5) - shorter descriptions
        worst_ever = [
            ("Mars of Destruction",
             "Amateur production with a confusing plot. Virtually no redeeming qualities.",
             "mars.jpg"),
            ("Skelter+Heaven",
             "Same issue as Mars of Destruction: weak animation and a nonsensical story.",
             "skelter.jpg"),
            ("Pupa",
             "Interesting premise, but terrible execution. Short episodes and excessive censorship.",
             "pupa.jpg"),
            ("Eiken",
             "Overloaded with pointless fanservice and no engaging story. Embarrassingly bad.",
             "eiken.jpg"),
            ("Vampire Holmes",
             "Promised mystery and vampires, delivered boredom and confusion.",
             "holmes.jpg")
        ]
        for title, desc, img in worst_ever:
            create_post(title, desc, cats['Worst of All Time'], img)

        # Best of This Year (Top 5)
        best_this_year = [
            ("Jujutsu Kaisen Season 3",
             "A solid continuation with insane battles and deep character development.",
             "jujutsu.jpg"),
            ("Solo Leveling",
             "Adaptation of the webtoon. The protagonist's power progression is addictive.",
             "sololeveling.jpg"),
            ("Chainsaw Man Season 2",
             "Insane, original, brutal, and captivating. Expands the bizarre universe.",
             "chainsaw2.jpg"),
            ("Vinland Saga Season 3",
             "Themes of peace and redemption. Matures with each season.",
             "vinland3.jpg"),
            ("Spy x Family Season 2",
             "Humor, action, and the tenderness of the most beloved fake family in anime.",
             "spyxfamily2.jpg")
        ]
        for title, desc, img in best_this_year:
            create_post(title, desc, cats['Best of the Year'], img)

        # Worst of This Year (Top 5)
        worst_this_year = [
            ("Zombie Idol Fever",
             "Attempt at zombie idols without any sense. Poor animation quality.",
             "zombieidol.jpg"),
            ("Love in the Outer Dimensions",
             "Tedious space romance with forced dialogue.",
             "loveouter.jpg"),
            ("Samurai Dentist",
             "Funny premise, failed execution. Repetitive humor.",
             "samuraidentist.jpg"),
            ("Kitten Warriors",
             "Poorly animated warrior cats. Could have been cute and childlike but failed.",
             "kitten.jpg"),
            ("Cyber Fairyland",
             "Cyberpunk mixed with fairies lacks cohesion. Promised innovation, delivered boredom.",
             "cyberfairyland.jpg")
        ]
        for title, desc, img in worst_this_year:
            create_post(title, desc, cats['Worst of the Year'], img)

        # Upcoming Releases (10 anime titles)
        future_releases = [
            ("Attack on Titan: A New Era", "A new saga following the end of the original. Expectation for continuous tension.", "aot_newera.jpg"),
            ("Demon Slayer: Pillar Chronicles", "Stories of the Hashira before the main storyline. Deeper character exploration.", "ds_pillar.jpg"),
            ("My Hero Academia: Final Arc", "Deku's final arc. An epic conclusion is expected.", "mha_final.jpg"),
            ("One Punch Man Season 3", "Insane battles and further character development.", "opm_s3.jpg"),
            ("Haikyuu!! Next Generation", "New volleyball players while maintaining the series' spirit.", "haikyuu_next.jpg"),
            ("Mushoku Tensei Season 3", "High-quality isekai with Rudeus' growth and a magical world.", "mushoku3.jpg"),
            ("Tokyo Revengers: The Final Time Leap", "A coherent conclusion to the time-travel saga. Tying up loose ends.", "tokyorev_final.jpg"),
            ("Chainsaw Man Season 3", "Expansion of the manga's insane universe. High expectations.", "chainsaw3.jpg"),
            ("Jujutsu Kaisen: Ancients", "Explores the sorcerers of the past. Expands the lore.", "jjk_ancients.jpg"),
            ("Sword Art Online: New Frontier", "A new era of VRMMO. Hopefully bringing freshness to the series.", "sao_newfrontier.jpg")
        ]
        for title, desc, img in future_releases:
            create_post(title, desc, cats['Upcoming Releases'], img)

        # Best Movies
        movies = [
            ("Your Name", "A story of love through time and space with impeccable animation.", "yourname.jpg"),
            ("Spirited Away", "Ghibli's masterpiece, a magical world full of metaphors.", "chihiro.jpg"),
            ("A Silent Voice", "Bullying, redemption, and acceptance. Emotionally powerful.", "vozsilencio.jpg"),
            ("Your Lie in April: The Movie", "A faithful adaptation of the musical drama. Emotionally impactful.", "yourlie.jpg"),
            ("Made in Abyss: Dawn of the Deep Soul", "A dark journey with stunning visuals that both shocks and enchants.", "madeinabyss.jpg")
        ]
        for title, desc, img in movies:
            create_post(title, desc, cats['Best Movies'], img)

        # Annual Winners
        winners = [
            ("Jujutsu Kaisen (2020)", "An impactful debut with fluid action and charisma.", "jujutsu2020.jpg"),
            ("Attack on Titan: The Final Season Part 1 (2021)", "Political tension and technical quality.", "aot2021.jpg"),
            ("Cyberpunk: Edgerunners (2022)", "Stylish, emotional, and inspired by the game.", "edgerunners2022.jpg"),
            ("Oshi no Ko (2023)", "Drama, mystery, and critique of the entertainment industry.", "oshinoko2023.jpg"),
            ("Solo Leveling (2024)", "A highly anticipated adaptation that lived up to the hype.", "sololeveling2024.jpg")
        ]
        for title, desc, img in winners:
            create_post(title, desc, cats['Annual Winners'], img)

        self.stdout.write(self.style.SUCCESS('Conteúdo de demonstração criado com sucesso!'))
