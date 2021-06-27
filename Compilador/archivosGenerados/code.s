.data
	var_x: .word 0:1
	var_y: .word 0:1
	var_z: .word 0:1
	var_a: .word 0:1
	var_b: .word 0:1
.text
main:
	li $a0,5
	sw  $a0  0($sp)
	addiu  $sp  $sp-4

	li $a0,2
 	lw $t1 4($sp)
	add $a0, $a0, $t1
 	addiu $sp $sp 4
	sw  $a0  0($sp)
	addiu  $sp  $sp-4

	li $a0,3
 	lw $t1 4($sp)
	sub $a0, $a0, $t1
 	addiu $sp $sp 4
	sw  $a0  0($sp)
	addiu  $sp  $sp-4

	li $a0,7
 	lw $t1 4($sp)
	mul $a0, $a0, $t1
 	addiu $sp $sp 4

	la  $t1, var_x
	sw  $a0, 0($t1)
	li $a0,2
	sw  $a0  0($sp)
	addiu  $sp  $sp-4

	li $a0,1
 	lw $t1 4($sp)
	div $a0, $a0, $t1
	mflo $a0
 	addiu $sp $sp 4

	la  $t1, var_y
	sw  $a0, 0($t1)
	li $a0,8
	sw  $a0  0($sp)
	addiu  $sp  $sp-4

	li $a0,2
 	lw $t1 4($sp)
	div $t1 $a0	mfhi $a0
 	addiu $sp $sp 4

	la  $t1, var_z
	sw  $a0, 0($t1)
	li $a0,1 

	la  $t1, var_a
	sw  $a0, 0($t1)
	li $a0,0 

	la  $t1, var_b
	sw  $a0, 0($t1)

 	jr $ra 