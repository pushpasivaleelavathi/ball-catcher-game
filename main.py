import pygame
import random
import sys
import asyncio

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Catcher")

clock = pygame.time.Clock()

# Images
bg = pygame.image.load("bg.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

basket_img = pygame.image.load("basket.png")
basket_img = pygame.transform.scale(basket_img, (100, 60))

# Fonts
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 70)

# Basket
basket = pygame.Rect(WIDTH // 2, HEIGHT - 80, 100, 60)
basket_speed = 8


def new_ball():
    return {
        "x": random.randint(50, WIDTH - 50),
        "y": -40,
        "speed": random.randint(4, 6),
        "color": (255, 255, 255)
    }


async def start_menu():

    while True:

        screen.blit(bg, (0, 0))

        title = big_font.render(
            "BALL CATCHER", True, (255, 255, 0)
        )

        start = font.render(
            "Press ENTER to Start", True, (255, 255, 255)
        )

        quit_t = font.render(
            "Press Q to Quit", True, (255, 0, 0)
        )

        screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, 200))
        )

        screen.blit(
            start,
            start.get_rect(center=(WIDTH // 2, 300))
        )

        screen.blit(
            quit_t,
            quit_t.get_rect(center=(WIDTH // 2, 350))
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return

                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        await asyncio.sleep(0)


async def game_over(score):

    while True:

        screen.fill((0, 0, 0))

        t1 = big_font.render(
            "GAME OVER", True, (255, 0, 0)
        )

        t2 = font.render(
            f"Score: {score}", True, (255, 255, 255)
        )

        t3 = font.render(
            "Press R to Restart", True, (200, 200, 200)
        )

        screen.blit(
            t1,
            t1.get_rect(center=(WIDTH // 2, 250))
        )

        screen.blit(
            t2,
            t2.get_rect(center=(WIDTH // 2, 320))
        )

        screen.blit(
            t3,
            t3.get_rect(center=(WIDTH // 2, 380))
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return

        await asyncio.sleep(0)


async def game():

    score = 0
    missed = 0
    level = 1
    paused = False

    ball = new_ball()

    powerup = None
    power_timer = 0

    while True:

        screen.blit(bg, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    paused = not paused

        if paused:

            pause_text = big_font.render(
                "PAUSED",
                True,
                (255, 255, 255)
            )

            screen.blit(
                pause_text,
                pause_text.get_rect(
                    center=(WIDTH // 2, 300)
                )
            )

            pygame.display.update()

            await asyncio.sleep(0)
            continue

        # Movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            basket.x -= basket_speed

        if keys[pygame.K_RIGHT]:
            basket.x += basket_speed

        basket.x = max(
            0,
            min(WIDTH - 100, basket.x)
        )

        # Ball falling
        ball["y"] += ball["speed"] + level

        pygame.draw.circle(
            screen,
            ball["color"],
            (ball["x"], int(ball["y"])),
            20
        )

        # Catch
        if basket.collidepoint(
            ball["x"],
            ball["y"]
        ):

            if powerup == "double":
                score += 2
            else:
                score += 1

            if random.random() < 0.3:

                powerup = random.choice(
                    ["slow", "double"]
                )

                power_timer = 300

            ball = new_ball()

        # Miss
        if ball["y"] > HEIGHT:

            missed += 1
            ball = new_ball()

        # Level
        level = score // 5 + 1

        # Powerup
        if powerup == "slow":

            ball["speed"] = max(
                2,
                ball["speed"] - 1
            )

        if powerup:

            power_timer -= 1

            if power_timer <= 0:
                powerup = None

        # Basket
        screen.blit(
            basket_img,
            (basket.x, basket.y)
        )

        # UI
        screen.blit(
            font.render(
                f"Score: {score}",
                True,
                (255, 255, 255)
            ),
            (10, 10)
        )

        screen.blit(
            font.render(
                f"Missed: {missed}",
                True,
                (255, 0, 0)
            ),
            (10, 50)
        )

        screen.blit(
            font.render(
                f"Level: {level}",
                True,
                (0, 255, 255)
            ),
            (10, 90)
        )

        if powerup:

            screen.blit(
                font.render(
                    f"Power: {powerup}",
                    True,
                    (255, 255, 0)
                ),
                (10, 130)
            )

        pygame.display.update()

        if missed >= 5:
            return score

        clock.tick(60)

        await asyncio.sleep(0)


async def main():

    while True:

        await start_menu()

        final_score = await game()

        await game_over(final_score)


asyncio.run(main())
