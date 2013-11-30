                                       -- Chapter 20 - Program 2
with Ada.Text_IO, Ada.Integer_Text_IO;
use Ada.Text_IO, Ada.Integer_Text_IO;

procedure Discrim2 is

   type SQUARE is array(INTEGER range <>,
                        INTEGER range <>) of INTEGER;

   type LINEAR_TYPE is array(INTEGER range <>) of POSITIVE;

   type STUFF(List_Size : POSITIVE) is
      record
         Matrix   : SQUARE(1..List_Size, 1..List_Size);
         Elements : INTEGER := List_Size * List_Size;
         Linear   : LINEAR_TYPE(1..List_Size);
         Number   : INTEGER := List_Size;
      end record;

   Data_Store  : STUFF(5);
   Big_Store   : STUFF(12);

   function Add_Elements(In_Array : STUFF) return INTEGER is
   Total : INTEGER := 0;
   begin
      for Index1 in In_Array.Matrix'RANGE(1) loop
         for Index2 in In_Array.Matrix'RANGE(2) loop
            Total := Total + In_Array.Matrix(Index1, Index2);
         end loop;
      end loop;
      return Total;
   end Add_Elements;

   procedure Set_To_Ones(Work_Array : in out STUFF) is
   begin
      for Index1 in Work_Array.Matrix'RANGE(1) loop
         for Index2 in Work_Array.Matrix'RANGE(2) loop
            Work_Array.Matrix(Index1, Index2) := 1;
         end loop;
      end loop;
   end Set_To_Ones;

begin

   for Index1 in 1..Data_Store.List_Size loop
      Data_Store.Linear(Index1) := Index1;
      for Index2 in 1..Data_Store.List_Size loop
         Data_Store.Matrix(Index1, Index2) := Index1 * Index2;
      end loop;
   end loop;

   Set_To_Ones(Big_Store);

   Put("The total of Data_Store is");
   Put(Add_Elements(Data_Store), 5);
   New_Line;

   Put("The total of Big_Store is ");
   Put(Add_Elements(Big_Store), 5);
   New_Line;

end Discrim2;




-- Result of execution

-- The total of Data_Store is   225
-- The total of Big_Store is    144
