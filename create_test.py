#!/usr/bin/env python3
"""
Add test for issue 481 to verify fix works
"""

import subprocess
import sys

# Create test file
test_code = '''import izumi.reflect.Tag

trait A {
  type T
}

trait AInt extends A {
  override type T = Int
}

trait ALong extends A {
  override type T = Long
}

trait AString extends A {
  override type T = String
}

object TestApp extends App {
  println("Test 1: AInt <:< A { type T = Int } (should be true)")
  val test1 = implicitly[AInt <:< A { type T = Int }]
  println(s"  Scala compiler result: $test1")
  
  val tagResult1 = Tag[AInt].tag <:< Tag[A { type T = Int }].tag
  println(s"  Tag result: $tagResult1")
  
  println("\\nTest 2: ALong <:< A { type T = Int } (should be false)")
  val test2 = implicitly[ALong <:< A { type T = Int }]
  println(s"  Scala compiler result: $test2")
  
  val tagResult2 = Tag[ALong].tag <:< Tag[A { type T = Int }].tag
  println(s"  Tag result: $tagResult2")
  
  println("\\nTest 3: AInt <:< A { type T = String } (should be false)")
  val test3 = implicitly[AInt <:< A { type T = String }]
  println(s"  Scala compiler result: $test3")
  
  val tagResult3 = Tag[AInt].tag <:< Tag[A { type T = String }].tag
  println(s"  Tag result: $tagResult3")
}
'''

with open("test_issue_481.scala", "w") as f:
    f.write(test_code)

print("Test file created")
