import SwiftUI
import Foundation


//Definition des Objekts "Bestellung"
struct Order: Codable {
    var auftraggeber: String? //auftraggeber
    var bearbeiter: String? //bearbeiter
    var bezeichnung: String? //bezeichnung
    var bestellnummer: String? //bestellnummer
    var bestelldatum: String? //bestelldatum
    var eingangsdatum: String? //eingangsdatim
    var liefertermin: String? //liefertermin
    var bezug: String? //bezug
    var fahrzeug_id: String?
    var fahrzeugkennung: String?//fahrzeug_id
    var lieferant: String? //lieferant
    var banf: String? //banf
    var bemerkung: String? //bemerkung
    var menge: Int? //menge
    var status: String? //status
    var teilenummer: String? //teilenummer
    var projekt: String? //projekt
    var id: Int? //id
    var liefertermin_status: String?
}

let sortedOrders = orders.sorted { (order1: Order, order2: Order) -> Bool in
    return order1.fahrzeugkennung < order2.fahrzeugkennung

// Ruft Skript-Funktion /update-order auf (PUT-Anfrage)
func updateOrder(id: Int, completion: @escaping (Bool) -> Void) {
    guard let url = URL(string: "http://53.45.164.52:12003/update-order") else {
        print("Ungültige URL.")
        return
    }

    var request = URLRequest(url: url)
    request.httpMethod = "PUT"

    let orderData: [String: Any] = ["id": id]

    do {
        let jsonData = try JSONSerialization.data(withJSONObject: orderData, options: [])
        request.httpBody = jsonData
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        // Fehler Handling
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Fehler beim Aktualisieren der Bestellung: \(error)")
                completion(false)
            } else if let response = response as? HTTPURLResponse, response.statusCode == 200 {
                print("Bestellung erfolgreich aktualisiert!")
                completion(true)
            } else {
                print("Fehler beim Aktualisieren der Bestellung.")
                completion(false)
            }
        }.resume()
    } catch {
        print("Fehler beim Erstellen der JSON-Daten: \(error)")
    }

}

// Filtert und sortiert Bestellungen
func filterOrdersByTeilenummer(Teilenummer: String, orders: [Order]) -> (filteredOrders: [Order], deliveredAlert: Bool) {
    var filteredOrders: [Order] = []
    var deliveredOrdersCount = 0

    for order in orders {
        if order.teilenummer == Teilenummer {
            if order.status == "offen" {
                filteredOrders.append(order)
            } else if order.status == "geliefert" {
                deliveredOrdersCount += 1
            }
        }
    }

    let deliveredAlert = filteredOrders.isEmpty && deliveredOrdersCount > 0
    return (filteredOrders, deliveredAlert)
}


// Funktion um Teilenummern umzuformatieren
func switchNr(Teilenummer: String) -> String {
    let newTeileNummer = Teilenummer.replacingOccurrences(of: " ", with: ".")
    return newTeileNummer
}

// Abfragen von Bestellungen - ruft Endpunkt /daten auf vom Skript (GET Anfrage)
func fetchOrdersByTeilenummer(teilenummer: String, completion: @escaping ([Order]?, String?) -> Void) {
    guard let urlStr = URL(string: "http://53.45.164.52:12003/daten?teilenummer=\(teilenummer)") else {
        print("Ungültige URL.")
        completion(nil, "Ungültige URL.")
        return
    }

    var request = URLRequest(url: urlStr)
    request.httpMethod = "GET"

    let task = URLSession.shared.dataTask(with: request) { data, response, error in
        guard let data = data, error == nil else {
            let errorMessage = "Fehler beim Laden der Daten: \(error?.localizedDescription ?? "Unbekannter Fehler")"
            completion(nil, errorMessage)
            return
        }

        do {
            let orders = try JSONDecoder().decode([Order].self, from: data)
            if orders.isEmpty {
                completion(nil, "Keine Bestellungen mit der Teilenummer \(teilenummer) gefunden.")
            } else {
                completion(orders, nil)
            }
        } catch {
            // Wenn dieser Fehler auftritt, kann es durchaus sein, dass Datentypen zwischen Server und App nicht übereinstimmen. z.B. String "1" und Int 1 kann schon den Fehler auslösen. Vollständigkeit von attributen im objekt überprüfen (app source code und server code), "?" steht bei den attributen für optional, so muss es auch im server definiert sein!
            let decodeErrorMessage = "Fehler beim Dekodieren der Daten: \(error.localizedDescription)"
            completion(nil, decodeErrorMessage)
        }
    }
    task.resume()
}
    func groupAndSortOrders(_ orders: [Order]) -> [String: [Order]] {
        let groupedOrders = Dictionary(grouping: orders, by: { $0.fahrzeugkennung ?? "" })
        let sortedGroupedOrders = groupedOrders.mapValues { (orders: [Order]) in
            orders.sorted { (order1: Order, order2: Order) -> Bool in
                return order1.someSortingCriterion < order2.someSortingCriterion
            }
        }
        return sortedGroupedOrders
    }



