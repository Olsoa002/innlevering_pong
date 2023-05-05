import pygame as pg

pg.init()

# Registrerer fonten som blir skrevet 
font20 = pg.font.Font('freesansbold.ttf', 20)

# definerer RGB som de primære fagene
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (255, 0, 0)

# enkle paramatere på skjermen
WIDTH, HEIGHT = 900, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pong")

# Definerer hvor fort ballen og tektanglene skal bevege seg ut ifra fps
klokke = pg.time.Clock()	
FPS = 50

# Rektangel classen 


class Rektangel:
		# Tar den opprinnelige posisjonen, dimensjonene, hastigheten og fargen til objektet
	def __init__(self, posx, posy, width, height, speed, color):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.speed = speed
		self.color = color
		# Rect som brukes til å kontrollere posisjonen og kollisjonen til objektet
		self.spillerRect = pg.Rect(posx, posy, width, height)
		# Objekter som blir visst på skjermen
		self.spiller = pg.draw.rect(screen, self.color, self.spillerRect)

	# Disse brukes til å hvise hva som skjer på skjermen
	def display(self):
		self.spiller = pg.draw.rect(screen, self.color, self.spillerRect)

	def update(self, yFac):
		self.posy = self.posy + self.speed*yFac

		# Begrenser striker til å være under toppen av skjermen
		if self.posy <= 0:
			self.posy = 0
		# Begrenser striker til å være over bunnen av skjermen
		elif self.posy + self.height >= HEIGHT:
			self.posy = HEIGHT-self.height

		# oppdaterer rect for de nye verdiene 
		self.spillerRect = (self.posx, self.posy, self.width, self.height)

	def displayScore(self, text, score, x, y, color):
		text = font20.render(text+str(score), True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)

	#blit definerer at teksten skal vises øvest på skjermen 

		screen.blit(text, textRect)

	def getRect(self):
		return self.spillerRect

# klassen til ballen


class Ball:
	def __init__(self, posx, posy, radius, speed, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac = 1
		self.ykollisjon = -1
		self.ball = pg.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)
		self.firstTime = 1

	def display(self):
		self.ball = pg.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		self.posx += self.speed*self.xFac
		self.posy += self.speed*self.ykollisjon

		# Hvis ballen treffer topp eller bunnflaten,
		# så endres tegnet til ykollisjon og
		# det resulterer i en refleksjon av ballen
		if self.posy <= 0 or self.posy >= HEIGHT:
			self.ykollisjon *= -1

		if self.posx <= 0 and self.firstTime:
			self.firstTime = 0
			return 1
		elif self.posx >= WIDTH and self.firstTime:
			self.firstTime = 0
			return -1
		else:
			return 0

	def reset(self):
		self.posx = WIDTH//2
		self.posy = HEIGHT//2
		self.xFac *= -1
		self.firstTime = 1

	# Disse brukes for å reflektere ballen når ballen treffer x-aksen
	def hit(self):
		self.xFac *= -1

	def getRect(self):
		return self.ball

# hoved funskjonen styrer hele spillet, når det skal starte og slutte
# hvor mange poeng spiller 1 og spiller 2 har
# kollisjon og refleksjon av ballen 
# hvordan tastene beveger de ulike rektanglene opp og ned


def hoved():
	running = True

	# Definerer objektene
	spiller1 = Rektangel(20, 0, 10, 100, 10, GREEN)
	spiller2 = Rektangel(WIDTH-30, 0, 10, 100, 10, GREEN)
	ball = Ball(250, 250, 20, 10, WHITE)

	liste_spillere = [spiller1, spiller2]

	# Definerer hvilken score spiller1 og spiller2 skal starte
	spiller1Score, spiller2Score = 0, 0
	spiller1YFac, spiller2YFac = 0, 0

	while running:
		screen.fill(BLACK)

		# For loop for selve kontrollene til spillet
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					spiller2YFac = -1
				if event.key == pg.K_DOWN:
					spiller2YFac = 1
				if event.key == pg.K_w:
					spiller1YFac = -1
				if event.key == pg.K_s:
					spiller1YFac = 1
			if event.type == pg.KEYUP:
				if event.key == pg.K_UP or event.key == pg.K_DOWN:
					spiller2YFac = 0
				if event.key == pg.K_w or event.key == pg.K_s:
					spiller1YFac = 0

		# for loop for kollisjonen til ballen
		for spiller in liste_spillere:
			if pg.Rect.colliderect(ball.getRect(), spiller.getRect()):
				ball.hit()

		# oppdaterer objektene
		spiller1.update(spiller1YFac)
		spiller2.update(spiller2YFac)
		point = ball.update()

		# -1 -> spiller 1 har fått poeng etter kollisjon
		# +1 -> spiller 2 har fått poeng etter kollisjon
		# 0 -> Ingen har fått poeng enda (ballen er fortsatt i spill)
		if point == -1:
			spiller1Score += 1
		elif point == 1:
			spiller2Score += 1

		# Når enten spiller 1 eller spiller har fått poeng
		# er ballen regnet som out of bouns
		# derfor bruker man denne if testen til å resette posisjonen til ballen 
		if point:
			ball.reset()

		# Hviser de ulike objektene på skjermen
		spiller1.display()
		spiller2.display()
		ball.display()

		# hviser score for spiller1 og spiller 2 på skjermen 
		spiller1.displayScore("Spiller 1 : ",
						spiller1Score, 100, 20, WHITE)
		spiller2.displayScore("spiller 2 : ",
						spiller2Score, WIDTH-100, 20, WHITE)

		pg.display.update()
		klokke.tick(FPS)	


if __name__ == "__main__":
	hoved()
	pg.quit()
