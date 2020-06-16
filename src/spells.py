#! /usr/bin/python3


enemy_name = ["slime", "goblin", "asdjfnbkjnbxiuxguawy", "bob", "self"]
target = ["above", "below", "beside", "at", "to", "towards", "through", "on"] #enemy name has to be the last word :)
spell = ["fireball", "icespike"]
action = ["throw", "yeet", "ride", "cast", "fire", "fling", "lob"]


def parse_command_string(p_action, p_spell, p_target, p_enemy_name):
  #This checks the current battle and sees if the spell/action is valid

  if ((p_action in action) and (p_spell in spell) and (p_target in target) and (p_enemy_name in enemy_name)):
    return True
  else:
    return False

  pass

def get_command_string():
  return input("Please enter an action: ")

def remove_spaces(in_string):
  out_string = ""
  for i in range(len(in_string)):
    if in_string[i] != ' ':
      out_string += in_string[i]
    else:
      continue
  return out_string

def command_parsing():

  space_at = []

  player_action = None
  player_spell = None
  player_target = None
  player_enemy_name = None

  command = get_command_string()
  print(command)

  #Get spaces, then seperates words
  command_list = command.split(' ')
  print(command_list)

  command_list = list(filter(None, command_list))

  player_action = command_list[0]
  player_spell  = command_list[1]
  player_target  = command_list[2]
  player_enemy_name  = command_list[3]


  print("Action :", player_action)
  print("Spell  :", player_spell)
  print("Target :", player_target)
  print("Enemy  :", player_enemy_name)


  if parse_command_string(player_action, player_spell, player_target, player_enemy_name):
    return 1
  else:
    return 0

def main():
  while True:
    if command_parsing():
      print("Success!")
    else:
      print("Oh fuck...")

if __name__ == "__main__":
  print("Actions: ", action)
  print("Spells : ", spell)
  print("Targets: ", target)
  print("Enemies: ", enemy_name)
  main()
