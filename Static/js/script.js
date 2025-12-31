function addPerson(){
    const container = document.getElementById("people");
    container.insertAdjacentHTML("beforeend", `
        <div class="row mb-2 person-entry">
            <div class="col">
                <input name="name" class="form-control" placeholder="Name" required>
            </div>
            <div class="col">
                <input name="amount" class="form-control" type="number" placeholder="Amount" required>
            </div>
        </div>
    `);
}