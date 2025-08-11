import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from blog.models import Category, Post


class Command(BaseCommand):
    """
    Command to create demo posts in the database based on provided content.
    It creates an author user (if it does not exist), categories, and posts
    under various categories, each with an associated image.
    """

    help = "Creates demo posts based on provided content."

    def handle(self, *args, **options):
        # Create an author user if it does not exist
        author, created = User.objects.get_or_create(username="admin")
        if created:
            author.set_password("admin")  # Use a secure password in production
            author.is_superuser = True
            author.is_staff = True
            author.save()
            self.stdout.write(self.style.SUCCESS("Admin user created."))

        # Define categories and their descriptions
        categories_data = {
            "Best of All Time": "Top Classic Anime",
            "Worst of All Time": "Worst Anime",
            "Best of the Year": "Top Anime of the Year",
            "Worst of the Year": "Worst Anime of the Year",
            "Upcoming Releases": "Anime Set to Premiere",
            "Best Movies": "Must-Watch Films",
            "Annual Winners": "Award-Winning Anime",
        }

        # Create categories
        cats = {}
        for name, desc in categories_data.items():
            c, _ = Category.objects.get_or_create(name=name, description=desc)
            cats[name] = c
            self.stdout.write(self.style.SUCCESS(f'Category "{name}" created.'))

        media_path = os.path.join(settings.MEDIA_ROOT, "posts")

        if not os.path.exists(media_path):
            self.stdout.write(self.style.ERROR("Media directory not found."))
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
            print(f"Looking for image at: {image_path}")

            if not os.path.exists(image_path):
                placeholder = "placeholder.jpg"
                image_path = os.path.join(media_path, placeholder)
                if not os.path.exists(image_path):
                    self.stdout.write(self.style.ERROR(f'Placeholder image "{placeholder}" not found.'))
                    return
                self.stdout.write(self.style.WARNING(f'Image "{image_name}" not found, using "{placeholder}".'))

            with open(image_path, "rb") as img_file:
                post = Post(title=title, content=content, author=author, category=category)
                post.cover_image.save(image_name, img_file, save=True)
            self.stdout.write(self.style.SUCCESS(f'Post "{title}" created.'))
            return post

        # Best of All Time (Top 5) - Complete Descriptions
        best_ever = [
            (
                "Fullmetal Alchemist: Brotherhood",
                (
                    "Fullmetal Alchemist: Brotherhood is often considered the "
                    "pinnacle of shounen anime. The story follows the Elric "
                    "brothers on a deep journey of redemption after a failed "
                    "attempt at human transmutation. Beyond its intense "
                    "adventure, the anime explores morality, sacrifice, and "
                    "the search for the meaning of life. Each character is "
                    "three-dimensional, and the balance between drama, humor, "
                    "and action is flawless. I recommend it for its captivating "
                    "storytelling, inspiring message, and notable technical "
                    "quality that remains consistent from start to finish."
                ),
                "fullmetal.jpg",
            ),
            (
                "Neon Genesis Evangelion",
                (
                    "Neon Genesis Evangelion revolutionized the mecha genre by "
                    "diving into the psyche of its characters. The series is "
                    "not just about giant robots but explores themes of "
                    "loneliness, fear of abandonment, and the search for "
                    "acceptance. Religious and philosophical symbolism permeates "
                    "every episode, creating multiple layers of interpretation. "
                    "The emotional claustrophobia and the tension between the "
                    "pilots and the NERV organization define the experience. I "
                    "recommend this anime for its bold narrative, cultural "
                    "influence, and the reflection it provokes on the human "
                    "condition."
                ),
                "evangelion.jpg",
            ),
            (
                "Monster",
                (
                    "Monster is a unique psychological thriller focused on the "
                    "pursuit between Dr. Tenma and the enigmatic Johan. Instead "
                    "of magic or special powers, the story is grounded in realism "
                    "and moral complexity. Each secondary character is carefully "
                    "constructed, adding depth to the world and the dilemmas faced. "
                    "The plot questions the value of life, the weight of "
                    "responsibility, and what makes us human. The slow and dense "
                    "narrative rewards the viewer with an intense and unforgettable "
                    "experience."
                ),
                "monster.jpg",
            ),
            (
                "Gintama",
                (
                    "Gintama is the perfect mix of comedy, satire, and action. "
                    "Set in a feudal Japan dominated by aliens, the series plays "
                    "with genre conventions, breaks the fourth wall, and makes "
                    "numerous pop culture references. But don’t be fooled: behind "
                    "the nonsensical humor, there are dramatic and emotional arcs "
                    "that explore loyalty, friendship, and redemption. The "
                    "characters are charismatic and evolve throughout the story. "
                    "Gintama surprises with its versatility, capable of making you "
                    "laugh uncontrollably and cry from pure emotion."
                ),
                "gintama.jpg",
            ),
            (
                "Death Note",
                (
                    "Death Note is an intellectual duel between two geniuses: Light "
                    "Yagami, who discovers a notebook capable of killing anyone whose "
                    "name is written in it, and L, the eccentric detective who tries to "
                    "stop him. The anime makes us question what justice is and how far "
                    "we can go to achieve it. The constant tension, dark atmosphere, and "
                    "meticulous strategies of the characters make every episode gripping. "
                    "The moral battle between absolute power and responsibility is its "
                    "greatest strength. I recommend it for its intensity and the ethical "
                    "reflection it inspires about humanity."
                ),
                "deathnote.jpg",
            ),
        ]
        for title, desc, img in best_ever:
            create_post(title, desc, cats["Best of All Time"], img)

        self.stdout.write(self.style.SUCCESS("Demo content created successfully!"))

        # Worst of All Time (Top 5) - shorter descriptions
        worst_ever = [
            (
                "TheMars of Destruction",
                (
                    "Mars of Destruction is an amateur production that unfortunately falls "
                    "short in several key areas. The plot is confusing and difficult to "
                    "follow, making it challenging for viewers to stay engaged with the "
                    "story. The animation quality is notably poor, reflecting the limited "
                    "resources and planning behind the project. Additionally, the characters "
                    "are underdeveloped, which prevents the audience from forming any "
                    "meaningful connections with them. The series lacks any redeeming "
                    "qualities, leaving little to captivate or retain the viewer's interest. "
                    "Overall, Mars of Destruction fails to deliver the elements that make an "
                    "anime memorable and enjoyable."
                ),
                "mars.jpg",
            ),
            (
                "Skelter+Heaven",
                (
                    "Skelter+Heaven suffers from many of the same issues as Mars of "
                    "Destruction, particularly weak animation and a nonsensical storyline. "
                    "The visual quality is subpar, with scenes appearing poorly animated and "
                    "inconsistent in style. The narrative is muddled and lacks clear "
                    "development, making it hard to grasp the overall premise or follow the "
                    "plot's progression. Moreover, the characters lack depth, preventing "
                    "viewers from becoming invested in their journeys. The absence of a "
                    "strong, coherent narrative direction makes Skelter+Heaven a frustrating "
                    "experience for those seeking a well-crafted anime."
                ),
                "skelter.jpg",
            ),
            (
                "Pupa",
                (
                    "Pupa offers an intriguing premise that blends elements of horror and "
                    "family drama, but its execution leaves much to be desired. The episodes "
                    "are notably short, limiting the ability to develop the story and "
                    "characters adequately. Additionally, excessive censorship detracts from "
                    "the intended emotional intensity and immersion, undermining the series' "
                    "impact. While the animation has its competent moments, it cannot "
                    "compensate for the narrative shortcomings. As a result, Pupa fails to "
                    "fully realize its potential, leaving viewers disappointed despite its "
                    "interesting concept."
                ),
                "pupa.jpg",
            ),
            (
                "Eiken",
                (
                    "Eiken is notorious for its overabundance of pointless fanservice, which "
                    "overshadows any attempt at crafting an engaging story. The series is "
                    "filled with sexually suggestive scenes that can alienate viewers looking "
                    "for a more substantial narrative. Beyond the fanservice, the storyline "
                    "itself is lackluster, offering little in terms of conflict or character "
                    "development. This combination makes Eiken an embarrassing entry in the "
                    "anime genre, as it struggles to balance visual entertainment with "
                    "meaningful content. Ultimately, Eiken fails to provide a satisfying "
                    "experience for audiences seeking quality storytelling."
                ),
                "eiken.jpg",
            ),
            (
                "Vampire Holmes",
                (
                    "Vampire Holmes promised a captivating blend of mystery and vampire lore "
                    "but ends up delivering a tedious and confusing experience. The plot is "
                    "poorly structured, with numerous loose ends that never come together "
                    "cohesively. Characters, including the protagonist, are superficial and "
                    "fail to evoke any genuine interest or empathy from the audience. While "
                    "the animation is competent, it cannot salvage the disorganized narrative. "
                    "Additionally, the mysteries introduced are not sufficiently developed, "
                    "making the series predictable and unengaging. Vampire Holmes does not "
                    "meet expectations, resulting in a lackluster and forgettable anime."
                ),
                "holmes.jpg",
            ),
        ]
        for title, desc, img in worst_ever:
            create_post(title, desc, cats["Worst of All Time"], img)

        # Best of This Year (Top 5) - Complete Descriptions
        best_this_year = [
            (
                "Jujutsu Kaisen Season 3",
                (
                    "Jujutsu Kaisen Season 3 continues the series with its trademark intense "
                    "battles and profound character development. This season delves deeper "
                    "into the intricate world of jujutsu sorcery, introducing new antagonists "
                    "and expanding on the lore that fans have come to love. The animation "
                    "quality remains exceptional, with fluid motion and vibrant visuals that "
                    "bring every fight scene to life. Character arcs are further explored, "
                    "allowing viewers to connect more deeply with their motivations and "
                    "backstories. Additionally, the storytelling balances dark themes with "
                    "moments of humor and camaraderie, maintaining the series' dynamic pacing. "
                    "Overall, Season 3 solidifies Jujutsu Kaisen as a standout in the shonen "
                    "genre, offering both excitement and emotional depth."
                ),
                "jujutsu.jpg",
            ),
            (
                "Solo Leveling",
                (
                    "Solo Leveling is a captivating adaptation of the popular webtoon, "
                    "faithfully translating its engaging storyline to the screen. The series "
                    "follows Sung Jin-Woo, the weakest hunter who gains the unique ability to "
                    "level up independently, making his power progression highly addictive to "
                    "watch. The animation effectively portrays intense battles and the "
                    "protagonist's growth, maintaining a high level of excitement throughout "
                    "the series. Character development is well-executed, showcasing Jin-Woo's "
                    "transformation from a struggling hunter to a formidable force. "
                    "Additionally, the world-building is intricate, providing a rich backdrop "
                    "for the action-packed narrative. Solo Leveling successfully captures the "
                    "essence of the webtoon, making it a must-watch for fans of the genre."
                ),
                "sololeveling.jpg",
            ),
            (
                "Chainsaw Man Season 2",
                (
                    "Chainsaw Man Season 2 continues to deliver its unique blend of insanity, "
                    "originality, and brutality, further expanding its bizarre universe. The "
                    "season delves deeper into the complex relationships between characters "
                    "and introduces new, intriguing personalities that add depth to the "
                    "storyline. The animation remains stunning, with dynamic action sequences "
                    "that are both brutal and visually captivating. The narrative explores "
                    "darker themes while maintaining a sense of dark humor, staying true to "
                    "the series' distinctive tone. As the universe expands, viewers are "
                    "treated to unexpected plot twists and creative world-building that keep "
                    "the story fresh and engaging. Overall, Season 2 enhances the Chainsaw Man "
                    "experience, making it a must-watch for fans of unconventional anime."
                ),
                "chainsaw2.jpg",
            ),
            (
                "Vinland Saga Season 3",
                (
                    "Vinland Saga Season 3 continues to explore profound themes of peace and "
                    "redemption, maturing with each new installment. The season delves into "
                    "the characters' internal struggles and their quests for personal and "
                    "societal reconciliation. The historical setting is meticulously crafted, "
                    "providing an authentic backdrop for the intricate political and emotional "
                    "narratives. Character development is at the forefront, with protagonists "
                    "and antagonists alike facing moral dilemmas that add layers to their "
                    "personalities. The animation quality remains high, capturing the gritty "
                    "and realistic tone of the series. Vinland Saga Season 3 solidifies its "
                    "place as a thoughtful and emotionally resonant epic, appealing to viewers "
                    "seeking depth and complexity in their anime."
                ),
                "vinland3.jpg",
            ),
            (
                "Spy x Family Season 2",
                (
                    "Spy x Family Season 2 continues to charm audiences with its perfect blend "
                    "of humor, action, and the heartfelt dynamics of the most beloved fake "
                    "family in anime. The season further develops the unique relationships "
                    "between the Forger family members, highlighting their individual strengths "
                    "and vulnerabilities. The action sequences are thrilling and well-paced, "
                    "seamlessly integrating with the comedic and emotional moments. The "
                    "animation is vibrant and expressive, bringing the characters' personalities "
                    "to life with great detail. The narrative balances espionage missions with "
                    "everyday family life, creating a harmonious mix that keeps the story "
                    "engaging. Spy x Family Season 2 is a delightful continuation that captures "
                    "the essence of what makes the series so endearing to fans."
                ),
                "spyxfamily2.jpg",
            ),
        ]
        for title, desc, img in best_this_year:
            create_post(title, desc, cats["Best of the Year"], img)

        # Worst of This Year (Top 5) - Complete Descriptions
        worst_this_year = [
            (
                "Zombie Idol Fever",
                (
                    "Zombie Idol Fever attempts to blend the unconventional concept of "
                    "zombie-themed idols but fails to execute it effectively. The animation "
                    "quality is subpar, with stiff movements and poorly designed characters "
                    "that detract from the overall viewing experience. The storyline lacks "
                    "coherence, making it difficult to follow the motivations and development "
                    "of the zombie idols. Additionally, the series struggles with pacing, "
                    "often dragging scenes that should be dynamic and engaging. The humor "
                    "and intended charm of the idol genre are lost amidst the disjointed "
                    "narrative. As a result, Zombie Idol Fever fails to deliver on its "
                    "unique premise, leaving viewers disappointed and uninterested."
                ),
                "zombieidol.jpg",
            ),
            (
                "Love in the Outer Dimensions",
                (
                    "Love in the Outer Dimensions presents a space romance that unfortunately "
                    "becomes tedious due to its forced dialogue and lackluster storytelling. "
                    "The romantic elements feel unnatural and contrived, preventing the "
                    "audience from forming a genuine emotional connection with the characters. "
                    "The setting, while initially promising, does not receive the depth and "
                    "exploration needed to make the space backdrop feel immersive and integral "
                    "to the plot. Additionally, the animation falls short in portraying the "
                    "vastness and beauty of outer space, making the environment feel flat and "
                    "uninspiring. The pacing is uneven, with slow-moving plot points that fail "
                    "to build tension or interest. Overall, Love in the Outer Dimensions "
                    "struggles to maintain engagement, resulting in a monotonous and "
                    "unremarkable romantic saga."
                ),
                "loveouter.jpg",
            ),
            (
                "Kitten Warriors",
                (
                    "Kitten Warriors features adorable warrior cats with the potential to be "
                    "both cute and action-packed, but the execution falls short due to poor "
                    "animation and underdeveloped characters. The animation quality is lacking, "
                    "with choppy movements and simplistic designs that fail to bring the warrior "
                    "kittens to life. The story does not provide enough depth or background, "
                    "making the characters' motivations and adventures feel superficial. "
                    "Additionally, the pacing is inconsistent, with action sequences that lack "
                    "excitement and dramatic tension. The intended childlike charm is overshadowed "
                    "by the lack of creativity and effort put into the series. Kitten Warriors "
                    "could have been an endearing and entertaining show but instead ends up being "
                    "a disappointing portrayal of what could have been a delightful concept."
                ),
                "kitten.jpg",
            ),
            (
                "Cyber Fairyland",
                (
                    "Cyber Fairyland attempts to merge cyberpunk aesthetics with fairy tale "
                    "elements, but the combination lacks cohesion and fails to create a "
                    "compelling narrative. The visual style is inconsistent, making it difficult "
                    "to establish a clear and engaging world for the story to unfold. The plot "
                    "promises innovation by blending two distinct genres, but the execution "
                    "results in a disjointed and uninteresting storyline. Character development "
                    "is sparse, leaving the protagonists and antagonists feeling flat and "
                    "unremarkable. Additionally, the pacing is slow, with little to no tension or "
                    "excitement to keep viewers invested. Instead of delivering a fresh and "
                    "imaginative experience, Cyber Fairyland ends up being a boring and uninspired "
                    "series that does not live up to its potential."
                ),
                "cyberfairyland.jpg",
            ),
        ]
        for title, desc, img in worst_this_year:
            create_post(title, desc, cats["Worst of the Year"], img)

        future_releases = [
            (
                "Attack on Titan: A New Era",
                (
                    "Attack on Titan: A New Era launches a fresh saga set after the "
                    "conclusion of the original series. Fans can anticipate the "
                    "continuation of the intense tension that 'Attack on Titan' is "
                    "renowned for, introducing new threats and challenges for the "
                    "protagonists to overcome. The animation is expected to uphold the "
                    "high visual standards that have made the series so acclaimed, with "
                    "dynamic battle scenes and intricate world-building. This new era will "
                    "delve deeper into the aftermath of the original storyline, exploring "
                    "the socio-political changes and the lingering effects of the Titan "
                    "conflict. Character development remains a focal point, providing "
                    "insights into the survivors' struggles and growth as they navigate a "
                    "transformed world. With high expectations, 'Attack on Titan: A New Era' "
                    "aims to revitalize the franchise and keep audiences engaged with its "
                    "compelling narrative and stunning visuals."
                ),
                "aot_newera.jpg",
            ),
            (
                "Demon Slayer: Pillar Chronicles",
                (
                    "Demon Slayer: Pillar Chronicles shifts the spotlight to the Hashira, "
                    "the elite warriors of the Demon Slayer Corps, before the events of the "
                    "main storyline. This spin-off promises a deeper exploration of the "
                    "characters who have captivated fans with their strength and dedication. "
                    "Each episode is expected to delve into the backstories of individual "
                    "Hashira, revealing their origins, motivations, and the personal battles "
                    "that shaped them into formidable demon slayers. The animation continues "
                    "to deliver the high-quality visuals and fluid action sequences that the "
                    "franchise is known for, enhancing the storytelling with breathtaking "
                    "fight scenes and emotional moments. By focusing on the Hashira's past, "
                    "the series aims to enrich the overall lore of 'Demon Slayer,' providing "
                    "fans with a more comprehensive understanding of the characters and the "
                    "world they inhabit. 'Pillar Chronicles' is set to deepen the connection "
                    "between the audience and their favorite warriors, adding layers of depth "
                    "to an already beloved series."
                ),
                "ds_pillar.jpg",
            ),
            (
                "My Hero Academia: Final Arc",
                (
                    "My Hero Academia: Final Arc marks the epic conclusion to Deku's journey "
                    "and the overarching narrative of the series. Fans can expect a grand "
                    "finale that resolves the major conflicts and challenges faced by the "
                    "heroes. This final arc is anticipated to feature intense battles, "
                    "strategic confrontations, and emotional resolutions as Deku and his "
                    "classmates strive to achieve their ultimate goals. The animation is set "
                    "to maintain the vibrant and dynamic style that has become synonymous "
                    "with 'My Hero Academia,' ensuring that every fight and heroic moment is "
                    "depicted with flair and excitement. Character development will reach its "
                    "peak, showcasing the growth and evolution of the protagonists as they "
                    "confront their greatest adversaries. Themes of legacy, sacrifice, and the "
                    "true meaning of heroism are expected to be prominently explored, "
                    "providing a satisfying and impactful conclusion to the beloved series. "
                    "'My Hero Academia: Final Arc' aims to leave a lasting impression, "
                    "celebrating the journey of its characters and the enduring spirit of "
                    "heroism."
                ),
                "mha_final.jpg",
            ),
            (
                "One Punch Man Season 3",
                (
                    "One Punch Man Season 3 continues to deliver the franchise's signature "
                    "blend of over-the-top battles and nuanced character development. Fans "
                    "can look forward to even more insane and visually spectacular fight "
                    "scenes as Saitama faces new and formidable opponents. This season is "
                    "expected to delve deeper into the backgrounds and motivations of both "
                    "heroes and villains, adding layers of complexity to the narrative. The "
                    "animation maintains its high energy and fluidity, enhancing the comedic "
                    "and action-packed moments that define the series. Additionally, new "
                    "characters are likely to be introduced, bringing fresh dynamics and "
                    "challenges to the existing roster. 'One Punch Man Season 3' aims to "
                    "balance humor with serious storytelling, ensuring that the series remains "
                    "as engaging and entertaining as ever. With continued character growth and "
                    "exhilarating battles, this season promises to keep fans on the edge of "
                    "their seats."
                ),
                "opm_s3.jpg",
            ),
            (
                "Haikyuu!! Next Generation",
                (
                    "Haikyuu!! Next Generation introduces a new cohort of volleyball "
                    "players while preserving the spirited and competitive essence of the "
                    "original series. The storyline follows young athletes aspiring to reach "
                    "the pinnacle of high school volleyball, facing various challenges both "
                    "on and off the court. The animation continues to excel in capturing the "
                    "intensity and dynamism of volleyball matches, with detailed and realistic "
                    "movements that bring the sport to life. Character development is a key "
                    "focus, showcasing the personal growth, teamwork, and perseverance of the "
                    "new generation of players. The series maintains the inspirational and "
                    "heartwarming themes that made 'Haikyuu!!' a favorite among fans, "
                    "emphasizing friendship, determination, and the love of the game. "
                    "'Haikyuu!! Next Generation' aims to attract both longtime enthusiasts and "
                    "new viewers by blending familiar elements with fresh narratives and "
                    "characters. This continuation promises to deliver the same high-energy "
                    "and emotionally resonant storytelling that defines the 'Haikyuu!!' "
                    "experience."
                ),
                "haikyuu_next.jpg",
            ),
            (
                "Mushoku Tensei Season 3",
                (
                    "Mushoku Tensei Season 3 continues the high-quality isekai adventure, "
                    "focusing on Rudeus' growth and his journey through a richly crafted "
                    "magical world. This season delves deeper into Rudeus' personal "
                    "development, exploring his abilities, relationships, and the challenges "
                    "he faces in a fantastical setting. The animation remains top-notch, "
                    "featuring intricate designs and fluid motion that enhance the immersive "
                    "experience of the magical realm. The narrative expands the lore of "
                    "'Mushoku Tensei,' introducing new regions, cultures, and mystical elements "
                    "that enrich the story. Character interactions and dynamics are further "
                    "explored, providing a deeper understanding of Rudeus and the people around "
                    "him. Additionally, new plotlines and conflicts emerge, driving the story "
                    "forward and keeping viewers engaged with ongoing adventures and emotional "
                    "arcs. 'Mushoku Tensei Season 3' promises to continue delivering a "
                    "captivating and enchanting isekai experience for its dedicated fanbase."
                ),
                "mushoku3.jpg",
            ),
            (
                "Tokyo Revengers: The Final Time Leap",
                (
                    "'Tokyo Revengers: The Final Time Leap' aims to provide a coherent and "
                    "satisfying conclusion to the time-travel saga that has captivated "
                    "audiences. This final installment seeks to tie up all loose ends, "
                    "resolving the intricate plotlines and character arcs that have been "
                    "developed throughout the series. The animation continues to deliver "
                    "intense and emotionally charged scenes, maintaining the high pace and "
                    "dramatic flair that fans have come to expect. The narrative focuses on "
                    "bringing closure to the protagonists' struggles, addressing the "
                    "consequences of their actions across different timelines. Themes of "
                    "redemption, friendship, and the impact of choices are expected to be "
                    "prominently featured, providing a meaningful and impactful resolution. "
                    "'The Final Time Leap' strives to deliver a memorable and fulfilling end "
                    "to the 'Tokyo Revengers' story, ensuring that fans leave with a sense "
                    "of completion and satisfaction."
                ),
                "tokyorev_final.jpg",
            ),
            (
                "Chainsaw Man Season 3",
                (
                    "'Chainsaw Man Season 3' expands the manga's already insane and "
                    "captivating universe, introducing new threats and deepening the existing "
                    "lore. This season continues to blend horror, action, and supernatural "
                    "elements in a unique and engaging manner. The animation remains visually "
                    "striking, with creative and intense fight sequences that highlight the "
                    "series' distinctive style. New characters are introduced, adding "
                    "complexity and fresh dynamics to the storyline, while returning "
                    "characters receive further development and exploration of their "
                    "backgrounds. The narrative delves into darker and more intricate "
                    "plotlines, maintaining the frenetic and unpredictable tone that fans "
                    "adore. Themes of power, identity, and survival are explored with depth "
                    "and nuance, providing a rich and immersive viewing experience. 'Chainsaw "
                    "Man Season 3' promises to elevate the series by pushing the boundaries "
                    "of its bizarre and thrilling universe, keeping audiences hooked with "
                    "every episode."
                ),
                "chainsaw3.jpg",
            ),
            (
                "Jujutsu Kaisen: Ancients",
                (
                    "'Jujutsu Kaisen: Ancients' delves into the history of sorcerers from the "
                    "past, significantly expanding the series' rich lore. This season explores "
                    "the origins of jujutsu techniques and the lives of the early sorcerers, "
                    "providing a deeper context for the current events and characters in the "
                    "main series. The animation continues to impress with its detailed and "
                    "fluid portrayal of supernatural battles and mystical settings. The "
                    "narrative weaves together elements of mystery and adventure, uncovering "
                    "ancient secrets that have long influenced the world of 'Jujutsu Kaisen.' "
                    "Character development is emphasized, offering insights into the "
                    "motivations and struggles of historical figures and their impact on the "
                    "present-day sorcerers. 'Ancients' enriches the overall storyline by "
                    "connecting past and present, enhancing the complexity and depth of the "
                    "series. Fans can expect a captivating exploration of the foundational "
                    "aspects of jujutsu, adding new dimensions to an already beloved anime."
                ),
                "jjk_ancients.jpg",
            ),
            (
                "Sword Art Online: New Frontier",
                (
                    "'Sword Art Online: New Frontier' ushers in a new era for the beloved "
                    "franchise, focusing on an innovative VRMMO experience. This season aims "
                    "to bring freshness to the series by introducing new game mechanics, "
                    "immersive worlds, and advanced technology that push the boundaries of "
                    "virtual reality storytelling. The animation continues to deliver "
                    "high-quality visuals, with detailed environments and dynamic action "
                    "sequences that enhance the sense of immersion. The narrative introduces "
                    "new characters and challenges, while maintaining connections to the "
                    "original storyline, creating a seamless blend of old and new elements. "
                    "Themes of technology, friendship, and survival are explored in depth, "
                    "providing both new and returning fans with engaging and thought-provoking "
                    "content. 'New Frontier' strives to expand the 'Sword Art Online' universe, "
                    "offering exciting adventures and emotional journeys that keep the spirit "
                    "of the original series alive. With its promise of innovation and "
                    "captivating storytelling, this new frontier aims to elevate the franchise "
                    "to new heights."
                ),
                "sao_newfrontier.jpg",
            ),
        ]
        for title, desc, img in future_releases:
            create_post(title, desc, cats["Upcoming Releases"], img)
        # Best Movies - Full Descriptions
        movies = [
            (
                "Your Name",
                (
                    "'Your Name' is a poignant story of love that transcends time and space, "
                    "beautifully brought to life with impeccable animation. Directed by "
                    "Makoto Shinkai, the film follows the intertwined lives of Taki and "
                    "Mitsuha, two teenagers who inexplicably begin to swap bodies "
                    "intermittently. This unique premise explores themes of connection, "
                    "fate, and the enduring power of love. The animation is nothing short "
                    "of stunning, with vibrant colors and meticulously crafted backgrounds "
                    "that enhance the emotional depth of the narrative. The seamless blend "
                    "of traditional animation with CGI elements creates visually mesmerizing "
                    "sequences that captivate audiences. The soundtrack, composed by RADWIMPS, "
                    "perfectly complements the film’s emotional beats, adding layers of "
                    "intensity and poignancy. 'Your Name' masterfully balances a heartfelt "
                    "romance with elements of mystery and fantasy, making it a universally "
                    "relatable and emotionally impactful cinematic experience."
                ),
                "yourname.jpg",
            ),
            (
                "Spirited Away",
                (
                    "'Spirited Away' stands as Studio Ghibli's masterpiece, immersing viewers "
                    "in a magical world rich with symbolism and metaphors. Directed by Hayao "
                    "Miyazaki, the film tells the enchanting tale of Chihiro, a young girl "
                    "who becomes trapped in a mysterious and otherworldly bathhouse inhabited "
                    "by spirits and magical creatures. As Chihiro navigates this fantastical "
                    "realm, she undergoes a profound journey of self-discovery, resilience, "
                    "and courage. The animation is exquisite, showcasing Studio Ghibli’s "
                    "signature attention to detail and imaginative character designs that "
                    "bring the spirit world to life. The narrative is layered with themes of "
                    "environmentalism, consumerism, and the loss of innocence, making it a "
                    "deeply thought-provoking experience. The film’s rich storytelling and "
                    "emotional depth resonate with audiences of all ages, solidifying "
                    "'Spirited Away' as a timeless classic that continues to inspire and "
                    "captivate."
                ),
                "chihiro.jpg",
            ),
            (
                "A Silent Voice",
                (
                    "'A Silent Voice' is an emotionally powerful film that delves into the "
                    "complex themes of bullying, redemption, and acceptance. Directed by "
                    "Naoko Yamada and based on the manga by Yoshitoki Ōima, the story centers "
                    "around Shōya Ishida, a former bully who seeks to make amends with Shōko "
                    "Nishimiya, a deaf girl he tormented during their childhood. The film "
                    "sensitively portrays the struggles of both characters as they navigate "
                    "their past traumas and strive for forgiveness and understanding. The "
                    "animation effectively captures the nuanced emotions of the characters, "
                    "using subtle visual cues and expressive character designs to convey their "
                    "internal conflicts. The soundtrack complements the narrative beautifully, "
                    "enhancing the film’s emotional resonance. 'A Silent Voice' is a heartfelt "
                    "exploration of the consequences of bullying and the importance of empathy "
                    "and reconciliation, offering a moving and thought-provoking viewing "
                    "experience."
                ),
                "vozsilencio.jpg",
            ),
            (
                "Your Lie in April: The Movie",
                (
                    "'Your Lie in April: The Movie' serves as a faithful adaptation of the "
                    "beloved musical drama series, delivering an emotionally impactful "
                    "continuation of the story. The film follows Kōsei Arima, a prodigious "
                    "pianist who has lost his ability to hear the sound of his piano after his "
                    "mother's death. His life takes a transformative turn when he meets Kaori "
                    "Miyazono, a spirited violinist whose free-spirited approach to music "
                    "reignites his passion for playing. The movie retains the series' stunning "
                    "animation, with beautifully rendered musical performances that capture "
                    "the intensity and emotion of each piece. The character development is "
                    "handled with care, deepening the viewers' connection to Kōsei and Kaori "
                    "as they navigate love, loss, and personal growth. The soundtrack, "
                    "featuring classical and original compositions, plays a pivotal role in "
                    "conveying the characters' emotions and the overarching themes of hope and "
                    "resilience. 'Your Lie in April: The Movie' successfully encapsulates the "
                    "essence of the series, offering a poignant and memorable cinematic "
                    "experience."
                ),
                "yourlie.jpg",
            ),
            (
                "Made in Abyss: Dawn of the Deep Soul",
                (
                    "'Made in Abyss: Dawn of the Deep Soul' takes viewers on a dark and "
                    "mesmerizing journey through the enigmatic Abyss, showcasing stunning "
                    "visuals that both shock and enchant. Directed by Masayuki Kojima and "
                    "produced by Kinema Citrus, the film continues the adventures of Riko, "
                    "Reg, and Nanachi as they delve deeper into the mysterious and perilous "
                    "Abyss in search of answers and survival. The animation is breathtaking, "
                    "with meticulously detailed environments that highlight the Abyss's "
                    "otherworldly beauty and hidden dangers. The film masterfully balances "
                    "moments of awe-inspiring wonder with intense and harrowing sequences, "
                    "creating a gripping and immersive experience. The narrative explores "
                    "themes of exploration, sacrifice, and the unyielding human spirit, adding "
                    "depth to the characters' motivations and the overarching lore of the "
                    "Abyss. 'Made in Abyss: Dawn of the Deep Soul' is a testament to the "
                    "series' ability to blend dark fantasy with emotional storytelling, making "
                    "it a standout addition to the franchise."
                ),
                "madeinabyss.jpg",
            ),
        ]
        for title, desc, img in movies:
            create_post(title, desc, cats["Best Movies"], img)

        # Annual Winners - Full Descriptions
        winners = [
            (
                "Jujutsu Kaisen (2020)",
                (
                    "'Jujutsu Kaisen' made a remarkable debut in 2020, quickly establishing "
                    "itself as a standout series in the shonen genre. The anime captivates "
                    "audiences with its fluid and dynamic action sequences, showcasing expertly "
                    "choreographed battles that are both visually stunning and strategically "
                    "engaging. The characters are imbued with charisma, each bringing a unique "
                    "personality and depth that resonates with viewers. The story delves into "
                    "the world of curses and sorcery, blending traditional supernatural elements "
                    "with fresh, innovative twists. The animation quality is consistently high, "
                    "with detailed backgrounds and smooth motion that enhance the overall viewing "
                    "experience. 'Jujutsu Kaisen' successfully balances intense action with "
                    "moments of humor and emotional depth, making it a compelling and impactful "
                    "series that continues to garner widespread acclaim."
                ),
                "jujutsu2020.jpg",
            ),
            (
                "Attack on Titan: The Final Season Part 1 (2021)",
                (
                    "'Attack on Titan: The Final Season Part 1' delivered a powerful culmination "
                    "to the long-running series, emphasizing political tension and high technical "
                    "quality. The season delves deeper into the complex socio-political dynamics "
                    "between different factions, adding layers of intrigue and strategic "
                    "maneuvering that elevate the narrative. The animation remains top-tier, with "
                    "meticulously detailed scenes that bring the intense battles and dramatic "
                    "moments to life with breathtaking realism. Character development is profound, "
                    "as key figures undergo significant transformations and confront their inner "
                    "conflicts. The storytelling is masterfully paced, balancing action-packed "
                    "sequences with thoughtful dialogue and emotional resonance. 'Attack on Titan: "
                    "The Final Season Part 1' sets a high bar for the concluding chapters, promising "
                    "a gripping and unforgettable finale for fans."
                ),
                "aot2021.jpg",
            ),
            (
                "Cyberpunk: Edgerunners (2022)",
                (
                    "'Cyberpunk: Edgerunners' stands out as a stylish and emotionally charged "
                    "adaptation inspired by the iconic video game. Set in the vibrant and "
                    "dystopian world of Night City, the series follows the journey of a young "
                    "street kid who becomes an edgerunner, a mercenary outlaw, seeking survival "
                    "and purpose. The animation is visually stunning, with a neon-soaked aesthetic "
                    "that perfectly captures the cyberpunk atmosphere. The storytelling is both "
                    "heartfelt and intense, exploring themes of ambition, identity, and the human "
                    "cost of technological advancement. The characters are well-developed, each "
                    "with their own compelling backstories and motivations that add depth to the "
                    "narrative. 'Cyberpunk: Edgerunners' successfully translates the essence of the "
                    "game into a captivating anime experience, balancing action with emotional "
                    "storytelling to create a memorable and impactful series."
                ),
                "edgerunners2022.jpg",
            ),
            (
                "Oshi no Ko (2023)",
                (
                    "'Oshi no Ko' presents a gripping narrative that intertwines drama, mystery, "
                    "and a critical look at the entertainment industry. The story follows the "
                    "lives of idols and their struggles behind the glamorous facade, delving into "
                    "the darker aspects of fame and the pressures faced by those in the spotlight. "
                    "The animation is beautifully crafted, with expressive character designs and "
                    "detailed settings that enhance the storytelling. The plot is intricately woven, "
                    "keeping viewers engaged with its twists and turns as it unravels the mysteries "
                    "surrounding the characters' lives. Themes of ambition, sacrifice, and the quest "
                    "for authenticity are explored with nuance, offering a thought-provoking critique "
                    "of the entertainment world. 'Oshi no Ko' stands out for its mature and layered "
                    "approach, making it a compelling watch for those interested in character-driven "
                    "dramas."
                ),
                "oshinoko2023.jpg",
            ),
            (
                "Solo Leveling (2024)",
                (
                    "'Solo Leveling' arrived in 2024 as a highly anticipated adaptation of the "
                    "popular webtoon, living up to the immense hype surrounding it. The series "
                    "follows Sung Jin-Woo, the weakest hunter who gains the unique ability to "
                    "level up independently, transforming him into an unstoppable force. The "
                    "animation is exceptional, capturing the intense and dynamic battles with "
                    "fluid motion and stunning visual effects that bring the action-packed scenes "
                    "to life. Character development is robust, showcasing Jin-Woo's growth from a "
                    "struggling hunter to a formidable hero, along with the evolution of supporting "
                    "characters who add depth to the story. The world-building is comprehensive, "
                    "with a richly detailed universe that expands the lore of the original webtoon. "
                    "'Solo Leveling' effectively balances thrilling action with engaging storytelling, "
                    "making it a standout addition to the action-fantasy genre and a must-watch for "
                    "fans of the source material."
                ),
                "sololeveling2024.jpg",
            ),
        ]
        for title, desc, img in winners:
            create_post(title, desc, cats["Annual Winners"], img)

        self.stdout.write(self.style.SUCCESS("Demo content created successfully!"))
